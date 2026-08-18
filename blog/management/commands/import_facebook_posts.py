"""นำเข้าโพสต์จากเพจ Facebook มาเป็น Post ในบล็อก

    python manage.py import_facebook_posts --since 2026-03-14 --until 2026-03-15 --dry-run
    python manage.py import_facebook_posts --since 7d

โพสต์ที่นำเข้าจะเป็น draft เสมอ (เว้นแต่สั่ง --status) ให้คนตรวจก่อนเผยแพร่
กันนำเข้าซ้ำด้วย Post.source_id ซึ่ง unique — รันกี่รอบก็ไม่ได้โพสต์ซ้ำ

credential อ่านตามลำดับนี้
  1. env FACEBOOK_PAGE_ID / FACEBOOK_PAGE_TOKEN
  2. ถ้าไม่มี จะดึงจาก Azure Bot channel ผ่าน az CLI (สะดวกตอนรันในเครื่อง)
"""

import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone as dt_timezone

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from blog.models import Post, PostType

GRAPH = "https://graph.facebook.com/v21.0/"
FIELDS = "id,message,created_time,full_picture,permalink_url,status_type"

# ความยาวหัวข้อสูงสุด — ตั้งไว้สั้นเพราะบรรทัดแรกของโพสต์เฟซบุ๊ก
# บ่อยครั้งเป็นย่อหน้าเต็ม ไม่ใช่หัวข้อ (Post.title รับได้ถึง 200)
TITLE_MAX = 60


def _az(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip()


def credentials_from_azure():
    """ดึง page id / token จาก Azure Bot channel — ใช้ตอนรันในเครื่องที่ az login แล้ว"""
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


def graph(path, params):
    url = GRAPH + path + "?" + urllib.parse.urlencode(params)
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


def first_line(message):
    for ln in (message or "").splitlines():
        ln = ln.strip()
        if ln:
            return ln
    return ""


def make_title(message, limit=TITLE_MAX):
    """บรรทัดแรกเป็นหัวข้อ ตัดที่ขอบเขตคำถ้ายาวเกิน

    ภาษาไทยไม่เว้นวรรคระหว่างคำ ถ้าหาช่องว่างใกล้ ๆ ไม่เจอก็ตัดตรง ๆ
    แล้วเติม … เพื่อให้เห็นว่าถูกตัด
    """
    line = first_line(message)
    if not line:
        return ""
    if len(line) <= limit:
        return line
    head = line[:limit]
    cut = max(head.rfind(" "), head.rfind("　"))
    # ยอมตัดที่ช่องว่างเฉพาะเมื่อไม่สั้นเกินไป ไม่งั้นหัวข้อจะกุดเกินไป
    if cut >= int(limit * 0.6):
        head = head[:cut]
    return head.rstrip(" ,.;:—-") + "…"


def to_html(message):
    """ข้อความธรรมดาจาก Facebook -> HTML สำหรับ RichTextUploadingField"""
    text = (message or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return ""
    blocks = [b.strip() for b in re.split(r"\n{2,}", text) if b.strip()]
    out = []
    for b in blocks:
        safe = html.escape(b).replace("\n", "<br>")
        out.append(f"<p>{safe}</p>")
    return "\n".join(out)


def parse_since(value):
    """รับได้ทั้ง '7d' และ '2026-03-14'"""
    if not value:
        return None
    m = re.fullmatch(r"(\d+)d", value.strip())
    if m:
        return (datetime.now(dt_timezone.utc) - timedelta(days=int(m.group(1)))).strftime("%Y-%m-%d")
    return value.strip()


class Command(BaseCommand):
    help = "นำเข้าโพสต์จากเพจ Facebook มาเป็นบทความ (draft) กันซ้ำด้วย source_id"

    def add_arguments(self, parser):
        parser.add_argument("--since", help="วันเริ่ม เช่น 2026-03-14 หรือ 7d")
        parser.add_argument("--until", help="วันสิ้นสุด เช่น 2026-03-15")
        parser.add_argument("--limit", type=int, default=50, help="ดึงมากสุดกี่โพสต์ (default 50)")
        parser.add_argument("--author", default="admin", help="username เจ้าของโพสต์ (default admin)")
        parser.add_argument("--post-type", default="Facebook Post", help="ชื่อ PostType")
        parser.add_argument("--status", default="draft", choices=["draft", "published", "archived"])
        parser.add_argument("--dry-run", action="store_true", help="แสดงผลอย่างเดียว ไม่เขียนฐานข้อมูล")

    def handle(self, *args, **o):
        page_id, token = credentials_from_azure()
        import os
        page_id = os.environ.get("FACEBOOK_PAGE_ID") or page_id
        token = os.environ.get("FACEBOOK_PAGE_TOKEN") or token
        if not page_id or not token:
            raise CommandError(
                "ไม่พบ credential — ตั้ง FACEBOOK_PAGE_ID / FACEBOOK_PAGE_TOKEN "
                "หรือ az login ให้เข้าถึง Azure Bot channel ได้"
            )

        dry = o["dry_run"]
        try:
            author = User.objects.get(username=o["author"])
        except User.DoesNotExist:
            raise CommandError(
                "ไม่พบ user '%s' — ระบุด้วย --author (มีอยู่: %s)"
                % (o["author"], ", ".join(User.objects.values_list("username", flat=True)[:5]))
            )
        post_type = PostType.objects.filter(name=o["post_type"]).first()

        params = {"fields": FIELDS, "limit": o["limit"], "access_token": token}
        since, until = parse_since(o.get("since")), o.get("until")
        if since:
            params["since"] = since
        if until:
            params["until"] = until

        self.stdout.write(
            "เพจ %s | ช่วง %s .. %s | ผู้เขียน %s | ประเภท %s | สถานะ %s%s"
            % (page_id, since or "-", until or "-", author.username,
               post_type.name if post_type else "(ไม่ระบุ)", o["status"],
               self.style.WARNING("  [DRY RUN]") if dry else "")
        )

        data, err = graph(f"{page_id}/posts", params)
        if err:
            raise CommandError("ดึงโพสต์ไม่สำเร็จ: %s" % err.get("error", {}).get("message", "")[:200])

        posts = data.get("data", [])
        if not posts:
            self.stdout.write(self.style.WARNING("ไม่มีโพสต์ในช่วงที่ระบุ"))
            return

        created = skipped = empty = 0
        for p in posts:
            fbid = p.get("id")
            message = p.get("message") or ""
            title = make_title(message)

            if not title:
                empty += 1
                self.stdout.write("  – ข้าม %s (ไม่มีข้อความ ทำหัวข้อไม่ได้)" % fbid)
                continue

            if Post.objects.filter(source_id=fbid).exists():
                skipped += 1
                self.stdout.write("  = มีอยู่แล้ว %s" % title[:55])
                continue

            published_at = None
            ct = p.get("created_time")
            if ct:
                try:
                    published_at = datetime.strptime(ct, "%Y-%m-%dT%H:%M:%S%z")
                except ValueError:
                    published_at = timezone.now()

            self.stdout.write(self.style.SUCCESS("  + %s" % title))
            self.stdout.write("      %s | %s ตัวอักษร | %s"
                              % (ct[:10] if ct else "-", len(message),
                                 "มีรูป" if p.get("full_picture") else "ไม่มีรูป"))

            if dry:
                created += 1
                continue

            with transaction.atomic():
                Post.objects.create(
                    title=title[:200],
                    author=author,
                    post_type=post_type,
                    content=to_html(message),
                    status=o["status"],
                    published_at=published_at,
                    meta_description=first_line(message)[:160],
                    source="facebook",
                    source_id=fbid,
                    source_url=p.get("permalink_url") or "",
                )
            created += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "%s %d โพสต์ | ข้ามเพราะมีอยู่แล้ว %d | ข้ามเพราะไม่มีข้อความ %d"
                % ("จะนำเข้า" if dry else "นำเข้าแล้ว", created, skipped, empty)
            )
        )
        if not dry and created:
            self.stdout.write("ทั้งหมดเป็น '%s' — ตรวจแล้วค่อยเผยแพร่ที่ /admin/blog/post/" % o["status"])
