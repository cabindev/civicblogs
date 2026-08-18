"""ย้ายโพสต์ที่จริง ๆ เป็น Reel จาก Post ไปเป็น Video

    python manage.py move_reels_to_video --dry-run
    python manage.py move_reels_to_video

การนำเข้ารอบแรกใส่ทุกอย่างลง Post รวมทั้ง Reel ซึ่งผิดกับที่ทีมทำไว้ —
วิดีโอของทีมอยู่ใน model Video แยกต่างหาก (video_url ชี้ไป facebook.com/reel/...)
คำสั่งนี้แก้ย้อนหลังให้ครั้งเดียว หลังจากนี้ import_facebook_posts
จะแยกปลายทางเองตาม media_type ที่ Graph API บอก

รูปหน้าปกถูก "คัดลอก" ไป blog/video_thumbnails/ ไม่ใช่แค่ชี้ path เดิม
เพื่อไม่ให้วิดีโอพังถ้าวันหลังมีคนล้างไฟล์กำพร้าใน featured_images/
"""

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import Post, Video

REEL_MARKERS = ("/reel/", "/videos/", "/watch")


class Command(BaseCommand):
    help = "ย้ายโพสต์ที่เป็น Reel จาก Post ไปเป็น Video (ครั้งเดียว)"

    def add_arguments(self, p):
        p.add_argument("--dry-run", action="store_true", help="แสดงผลอย่างเดียว ไม่แก้ฐานข้อมูล")
        p.add_argument("--keep-posts", action="store_true",
                       help="ไม่ลบ Post ต้นทางหลังย้าย (ใช้ตรวจสอบก่อน)")

    def handle(self, *a, **o):
        dry = o["dry_run"]

        qs = Post.objects.filter(source="facebook")
        reels = [p for p in qs if any(m in (p.source_url or "") for m in REEL_MARKERS)]

        self.stdout.write("โพสต์ที่นำเข้าทั้งหมด %d | เป็น Reel %d | คงไว้ใน Post %d%s"
                          % (qs.count(), len(reels), qs.count() - len(reels),
                             self.style.WARNING("  [DRY RUN]") if dry else ""))
        if not reels:
            self.stdout.write(self.style.WARNING("ไม่มีอะไรต้องย้าย"))
            return

        moved = skipped = no_thumb = 0
        for p in reels:
            if Video.objects.filter(source_id=p.source_id).exists():
                skipped += 1
                continue

            self.stdout.write("  → %s" % p.title[:62])
            if dry:
                moved += 1
                continue

            with transaction.atomic():
                v = Video.objects.create(
                    title=p.title,
                    description=p.content,
                    video_url=p.source_url,
                    category=p.category,
                    author=p.author,
                    status=p.status,
                    published_at=p.published_at,
                    thumbnail_alt=p.featured_image_alt or p.title[:200],
                    source="facebook",
                    source_id=p.source_id,
                )
                # คัดลอกไฟล์รูป ไม่ใช่ชี้ path เดิม
                if p.featured_image:
                    try:
                        p.featured_image.open("rb")
                        data = p.featured_image.read()
                        p.featured_image.close()
                        v.thumbnail.save(p.featured_image.name.split("/")[-1],
                                         ContentFile(data), save=True)
                    except Exception as e:
                        no_thumb += 1
                        self.stdout.write(self.style.WARNING(
                            "      คัดลอกรูปไม่สำเร็จ: %s" % str(e)[:70]))
                else:
                    no_thumb += 1

                if not o["keep_posts"]:
                    p.delete()
            moved += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            "%s %d รายการ | ข้ามเพราะมีอยู่แล้ว %d | ไม่มีรูป %d"
            % ("จะย้าย" if dry else "ย้ายแล้ว", moved, skipped, no_thumb)))
        if not dry:
            self.stdout.write("Post ที่เหลือจากการนำเข้า : %d"
                              % Post.objects.filter(source="facebook").count())
            self.stdout.write("Video ที่มาจากการนำเข้า  : %d"
                              % Video.objects.filter(source="facebook").count())
