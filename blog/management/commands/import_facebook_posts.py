"""นำเข้าโพสต์จากเพจ Facebook มาเป็น Post ในบล็อก

    python manage.py import_facebook_posts --since 2026-03-14 --until 2026-03-15 --dry-run
    python manage.py import_facebook_posts --since 7d --status published

กันนำเข้าซ้ำด้วย Post.source_id ซึ่ง unique — รันกี่รอบก็ไม่ได้โพสต์ซ้ำ
จึงปลอดภัยพอจะตั้ง cron หรือให้ agent สั่งรัน

สิ่งที่เดาให้อัตโนมัติ
  - category : จับคู่จากคำสำคัญในเนื้อหา (วัดกับโพสต์ที่คนจัดไว้แล้วได้ 97%)
               ถ้าไม่มั่นใจจะปล่อยว่าง ไม่เดามั่ว
  - post type: อ่านจาก media_type ที่ Graph API บอก (video/photo/album/link)
               แม่นยำเพราะ API บอกเอง ไม่ใช่การเดา
  - รูปหน้าปก : โหลดจาก full_picture (วิดีโอจะได้ thumbnail)

credential อ่านตามลำดับ
  1. env FACEBOOK_PAGE_ID / FACEBOOK_PAGE_TOKEN
  2. ถ้าไม่มี ดึงจาก Azure Bot channel ผ่าน az CLI (สะดวกตอนรันในเครื่อง)
"""

import html
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone as dt_timezone

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from blog.models import Category, Post, PostType

GRAPH = "https://graph.facebook.com/v21.0/"
FIELDS = ("id,message,created_time,status_type,full_picture,permalink_url,"
          "attachments{media_type,type}")

# หัวข้อมาจากบรรทัดแรกของโพสต์ ซึ่งบ่อยครั้งเป็นย่อหน้าเต็มไม่ใช่หัวข้อ
# จึงตัดสั้นกว่าที่ Post.title รับได้ (200) มาก
TITLE_MAX = 60

# คำสำคัญ -> ชื่อ Category ที่มีอยู่ในระบบ
# ตั้งตามชื่อพื้นที่/ประเด็นของแต่ละโปรเจค CivicSpace
CATEGORY_KEYWORDS = {
    "กระทงสาย": ["กระทงสาย", "จังหวัดตาก", "เมืองตาก"],
    "งานช้าง": ["ช้าง", "สุรินทร์"],
    "เด็กน่านโตที่นี่ได้ไหม": ["น่าน"],
    "เดือนสิบเมืองคอน": ["เดือนสิบ", "นครศรี", "เมืองคอน", "สารทเดือนสิบ"],
    "บวชสร้างสุข วิถีอ่างทอง": ["บวช", "อ่างทอง"],
    "เปลี่ยนค่านิยมงานศพ": ["งานศพ", "ฌาปน", "เผาศพ", "ศพ"],
    "เผาเทียนเล่นไฟสุโขทัย": ["สุโขทัย", "เผาเทียน"],
    "ยี่เป็งเชียงใหม่": ["ยี่เป็ง", "เชียงใหม่"],
    "เยาวชนสุขเกินร้อย": ["ร้อยเอ็ด", "สุขเกินร้อย"],
}

# media_type จาก Graph -> ชื่อ PostType ที่อยากใช้ เรียงตามลำดับความชอบ
# ถ้าไม่มี PostType ชื่อนั้นในระบบจะตกไปใช้ค่า --post-type
# หมายเหตุ: แยก "Infographic" กับ "Article" จาก API ไม่ได้ ทั้งคู่เป็น photo เหมือนกัน
# จึงไม่เดา ปล่อยให้เป็น Facebook Post แล้วให้คนมาแก้เอง
MEDIA_TO_POSTTYPE = {
    "video": ["Video", "Facebook Post"],
    "link": ["News", "Facebook Post"],
}


def _az(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


def credentials_from_azure():
    sub = _az("az account show --query id -o tsv")
    if not sub:
        return None, None
    url = (
        f"https://management.azure.com/subscriptions/{sub}/resourceGroups/civicspace_group"
        f"/providers/Microsoft.BotService/botServices/civic-bot"
        f"/channels/FacebookChannel/listChannelWithKeys?api-version=2022-09-15"
    )
    raw = _az(f'az rest --method post --url "{url}" 2>/dev/null')
    if not raw:
        return None, None
    try:
        p = json.loads(raw)["properties"]["properties"]
        page = (p.get("pages") or [{}])[0]
        return str(page.get("id") or ""), page.get("accessToken") or ""
    except Exception:
        return None, None


def _fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        try:
            return None, json.load(e)
        except Exception:
            return None, {"error": {"message": e.read().decode()[:250]}}
    except Exception as e:
        return None, {"error": {"message": str(e)[:250]}}


def graph(path, params):
    return _fetch(GRAPH + path + "?" + urllib.parse.urlencode(params))


def first_line(message):
    for ln in (message or "").splitlines():
        ln = ln.strip()
        if ln:
            return ln
    return ""


def make_title(message, limit=TITLE_MAX):
    """บรรทัดแรกเป็นหัวข้อ ตัดที่ขอบเขตคำถ้ายาวเกิน

    ภาษาไทยไม่เว้นวรรคระหว่างคำ ถ้าหาช่องว่างใกล้ ๆ ไม่เจอก็ตัดตรง ๆ
    """
    line = first_line(message)
    if not line:
        return ""
    if len(line) <= limit:
        return line
    head = line[:limit]
    cut = max(head.rfind(" "), head.rfind("　"))
    if cut >= int(limit * 0.6):
        head = head[:cut]
    return head.rstrip(" ,.;:—-") + "…"


def starts_with_quote(title):
    """หัวข้อที่เป็นคำพูดอ้างอิง — อาจอ่านผิดความหมายเมื่อยืนเดี่ยวบนหน้าเว็บ"""
    return bool(title) and title.lstrip()[:1] in '“"\'‘'


def to_html(message):
    text = (message or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return ""
    blocks = [b.strip() for b in re.split(r"\n{2,}", text) if b.strip()]
    return "\n".join("<p>%s</p>" % html.escape(b).replace("\n", "<br>") for b in blocks)


def guess_category(text):
    """เดา Category จากคำสำคัญ — คืน None ถ้าไม่มีคำไหนตรงเลย (ไม่เดามั่ว)"""
    plain = re.sub(r"<[^>]+>", " ", text or "")
    best, score = None, 0
    for name, kws in CATEGORY_KEYWORDS.items():
        s = sum(plain.count(k) for k in kws)
        if s > score:
            best, score = name, s
    return best


def media_type_of(post):
    att = (post.get("attachments") or {}).get("data") or [{}]
    return att[0].get("media_type") or ""


def parse_since(value):
    if not value:
        return None
    m = re.fullmatch(r"(\d+)d", value.strip())
    if m:
        return (datetime.now(dt_timezone.utc) - timedelta(days=int(m.group(1)))).strftime("%Y-%m-%d")
    return value.strip()


class Command(BaseCommand):
    help = "นำเข้าโพสต์จากเพจ Facebook มาเป็นบทความ กันซ้ำด้วย source_id"

    def add_arguments(self, p):
        p.add_argument("--since", help="วันเริ่ม เช่น 2026-03-14 หรือ 7d")
        p.add_argument("--until", help="วันสิ้นสุด เช่น 2026-03-20")
        p.add_argument("--limit", type=int, default=100, help="ขนาดต่อหน้าที่ขอจาก Graph")
        p.add_argument("--max", type=int, default=None, dest="max_posts",
                       help="จำกัดจำนวนที่นำเข้า (ไม่ใส่ = ทั้งหมด)")
        p.add_argument("--author", default="admin", help="username เจ้าของโพสต์")
        p.add_argument("--post-type", default="Facebook Post", help="PostType เมื่อเดาไม่ได้")
        p.add_argument("--status", default="draft", choices=["draft", "published", "archived"])
        p.add_argument("--no-images", action="store_true", help="ไม่ต้องโหลดรูปหน้าปก")
        p.add_argument("--no-category", action="store_true", help="ไม่ต้องเดา category")
        p.add_argument("--newest-first", action="store_true",
                       help="เรียงใหม่->เก่า (ปกติเรียงเก่า->ใหม่ตาม timeline คอนเทนต์)")
        p.add_argument("--dry-run", action="store_true", help="แสดงผลอย่างเดียว ไม่เขียนฐานข้อมูล")

    def handle(self, *a, **o):
        page_id, token = credentials_from_azure()
        page_id = os.environ.get("FACEBOOK_PAGE_ID") or page_id
        token = os.environ.get("FACEBOOK_PAGE_TOKEN") or token
        if not page_id or not token:
            raise CommandError("ไม่พบ credential — ตั้ง FACEBOOK_PAGE_ID / FACEBOOK_PAGE_TOKEN "
                               "หรือ az login ให้เข้าถึง Azure Bot channel")

        dry = o["dry_run"]
        try:
            author = User.objects.get(username=o["author"])
        except User.DoesNotExist:
            raise CommandError("ไม่พบ user '%s' (มีอยู่: %s)" % (
                o["author"], ", ".join(User.objects.values_list("username", flat=True)[:5])))

        fallback_type = PostType.objects.filter(name=o["post_type"]).first()
        types_by_name = {t.name: t for t in PostType.objects.all()}
        cats_by_name = {c.name: c for c in Category.objects.all()}

        params = {"fields": FIELDS, "limit": o["limit"], "access_token": token}
        since, until = parse_since(o.get("since")), o.get("until")
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        self.stdout.write("เพจ %s | ช่วง %s .. %s | ผู้เขียน %s | สถานะ %s%s" % (
            page_id, since or "-", until or "-", author.username, o["status"],
            self.style.WARNING("  [DRY RUN]") if dry else ""))

        # ---- ดึงโพสต์ (ไล่ paging) ----
        posts, next_url, pages = [], None, 0
        while True:
            data, err = _fetch(next_url) if next_url else graph(f"{page_id}/posts", params)
            if err:
                raise CommandError("ดึงโพสต์ไม่สำเร็จ: %s"
                                   % err.get("error", {}).get("message", "")[:200])
            batch = data.get("data", [])
            posts.extend(batch)
            pages += 1
            next_url = (data.get("paging") or {}).get("next")
            if not next_url or not batch or pages >= 20:
                break
        if not posts:
            self.stdout.write(self.style.WARNING("ไม่มีโพสต์ในช่วงที่ระบุ"))
            return

        # Graph คืนโพสต์ใหม่สุดก่อน แต่เราต้องการไล่ตาม timeline ของคอนเทนต์
        # เรียงเก่า -> ใหม่ เพื่อให้ --max หยิบโพสต์ที่ถัดจาก --since จริง ๆ
        if not o["newest_first"]:
            posts.sort(key=lambda x: x.get("created_time") or "")
        self.stdout.write("ดึงมาได้ %d โพสต์ (%d หน้า) — เรียง %s\n" % (
            len(posts), pages, "ใหม่->เก่า" if o["newest_first"] else "เก่า->ใหม่"))

        created = skipped = empty = 0
        quote_titles, no_category, forced_draft, no_image = [], [], [], 0

        for p in posts:
            if o["max_posts"] and created >= o["max_posts"]:
                break

            fbid = p.get("id")
            message = p.get("message") or ""
            title = make_title(message)

            if not title:
                empty += 1
                continue
            if Post.objects.filter(source_id=fbid).exists():
                skipped += 1
                continue

            mtype = media_type_of(p)
            ptype = fallback_type
            for name in MEDIA_TO_POSTTYPE.get(mtype, []):
                if name in types_by_name:
                    ptype = types_by_name[name]
                    break

            cat = None
            if not o["no_category"]:
                guessed = guess_category(message)
                cat = cats_by_name.get(guessed) if guessed else None
                if cat is None:
                    no_category.append(title)

            published_at = None
            ct = p.get("created_time")
            if ct:
                try:
                    published_at = datetime.strptime(ct, "%Y-%m-%dT%H:%M:%S%z")
                except ValueError:
                    published_at = timezone.now()

            if starts_with_quote(title):
                quote_titles.append(title)

            # หน้าเว็บ Next.js อ่าน category.name ตรง ๆ หลายจุดโดยไม่กัน null
            # โพสต์ published ที่ไม่มี category จึงทำให้หน้าแรกทั้งหน้าพัง
            # กันไว้ที่ต้นทาง: ถ้าไม่มี category ให้เป็น draft เสมอ
            row_status = o["status"]
            if cat is None and row_status == "published":
                row_status = "draft"
                forced_draft.append(title)

            pic = p.get("full_picture")
            if not pic:
                no_image += 1

            self.stdout.write(self.style.SUCCESS("  + %s" % title))
            self.stdout.write("      %s | %s | %s | %s" % (
                ct[:10] if ct else "-",
                mtype or "ไม่ระบุ",
                ptype.name if ptype else "ไม่ระบุประเภท",
                cat.name if cat else self.style.WARNING("ไม่มี category")))

            created += 1
            if dry:
                continue

            with transaction.atomic():
                post = Post.objects.create(
                    title=title[:200],
                    author=author,
                    category=cat,
                    post_type=ptype,
                    content=to_html(message),
                    status=row_status,
                    published_at=published_at,
                    meta_description=first_line(message)[:160],
                    source="facebook",
                    source_id=fbid,
                    source_url=p.get("permalink_url") or "",
                )
                if pic and not o["no_images"]:
                    try:
                        req = urllib.request.Request(pic, headers={"User-Agent": "civicblogs-import"})
                        with urllib.request.urlopen(req, timeout=60) as r:
                            blob = r.read()
                        post.featured_image.save("fb_%s.jpg" % fbid.split("_")[-1],
                                                 ContentFile(blob), save=True)
                        post.featured_image_alt = title[:200]
                        post.save(update_fields=["featured_image_alt"])
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            "      โหลดรูปไม่สำเร็จ: %s" % str(e)[:80]))

        # ---- สรุป ----
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            "%s %d โพสต์ | ข้ามเพราะมีอยู่แล้ว %d | ข้ามเพราะไม่มีข้อความ %d"
            % ("จะนำเข้า" if dry else "นำเข้าแล้ว", created, skipped, empty)))

        if no_category:
            self.stdout.write(self.style.WARNING(
                "\nไม่มี category %d โพสต์ (เดาไม่ได้ ปล่อยว่างไว้ให้เติมเอง):" % len(no_category)))
            for t in no_category[:8]:
                self.stdout.write("   – %s" % t)

        if forced_draft:
            self.stdout.write(self.style.WARNING(
                "\nบังคับเป็น draft %d โพสต์ (ไม่มี category)" % len(forced_draft)))
            self.stdout.write(
                "   หน้าเว็บอ่าน category.name โดยไม่กัน null — โพสต์ published ที่ไม่มี")
            self.stdout.write(
                "   category จะทำให้หน้าแรกพังทั้งหน้า เลือก category แล้วค่อยเผยแพร่")

        if quote_titles:
            self.stdout.write(self.style.WARNING(
                "\n⚠️  หัวข้อที่ขึ้นต้นด้วยเครื่องหมายคำพูด %d โพสต์" % len(quote_titles)))
            self.stdout.write(
                "   มักเป็นวาทะที่โพสต์กำลังวิพากษ์ ถ้าเผยแพร่จะอ่านผิดความหมายได้")
            for t in quote_titles[:8]:
                self.stdout.write("   – %s" % t)

        if no_image:
            self.stdout.write("\nไม่มีรูปให้ใช้ %d โพสต์" % no_image)
