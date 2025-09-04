from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate database with sample blog data'

    def handle(self, *args, **options):
        
        # Create categories
        categories_data = [
            {'name': 'เทคโนโลยี', 'slug': 'technology', 'description': 'ข่าวสารและบทความเกี่ยวกับเทคโนโลยี'},
            {'name': 'การเมือง', 'slug': 'politics', 'description': 'ข่าวการเมืองและประชาธิปไตย'},
            {'name': 'สังคม', 'slug': 'society', 'description': 'ประเด็นสังคมและการใช้ชีวิต'},
            {'name': 'สิ่งแวดล้อม', 'slug': 'environment', 'description': 'ปัญหาสิ่งแวดล้อมและการอนุรักษ์'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'slug': cat_data['slug'], 'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get superuser
        try:
            admin_user = User.objects.get(email='evo_reaction@hotmail.com')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Superuser not found'))
            return

        # Create sample posts
        posts_data = [
            {
                'title': 'ยินดีต้อนรับสู่ CivicBlogs',
                'excerpt': 'แพลตฟอร์มใหม่สำหรับการแสดงความคิดเห็นและการสื่อสารของประชาชน',
                'content': '''<h2>ยินดีต้อนรับสู่ CivicBlogs</h2>
                
                <p>CivicBlogs เป็นแพลตฟอร์มที่สร้างขึ้นเพื่อเป็นพื้นที่สำหรับประชาชนในการแสดงความคิดเห็น แลกเปลี่ยนทัศนะ และสื่อสารในประเด็นต่างๆ ที่เกี่ยวข้องกับสังคมและประชาธิปไตย</p>
                
                <h3>จุดมุ่งหมายของเรา</h3>
                <ul>
                    <li>สร้างพื้นที่สำหรับการแสดงความคิดเห็นอย่างเสรี</li>
                    <li>ส่งเสริมการมีส่วนร่วมของประชาชน</li>
                    <li>เป็นแหล่งข้อมูลข่าวสารที่เชื่อถือได้</li>
                </ul>
                
                <p>เราหวังว่าแพลตฟอร์มนี้จะเป็นประโยชน์ต่อทุกคน</p>''',
                'category': Category.objects.get(name='สังคม'),
                'status': 'published'
            },
            {
                'title': 'การใช้เทคโนโลยีในการมีส่วนร่วมทางการเมือง',
                'excerpt': 'เทคโนโลยีสามารถช่วยให้ประชาชนมีส่วนร่วมในกระบวนการประชาธิปไตยได้มากขึ้น',
                'content': '''<h2>เทคโนโลยีกับประชาธิปไตย</h2>
                
                <p>ในยุคดิจิทัล เทคโนโลยีได้กลายเป็นเครื่องมือสำคัญในการส่งเสริมการมีส่วนร่วมของประชาชนในกระบวนการประชาธิปไตย</p>
                
                <h3>ประโยชน์ของเทคโนโลยี</h3>
                <ol>
                    <li>เข้าถึงข้อมูลได้ง่ายขึ้น</li>
                    <li>สามารถแสดงความคิดเห็นได้รวดเร็ว</li>
                    <li>ลดอุปสรรคในการเข้าถึงกระบวนการทางการเมือง</li>
                </ol>
                
                <p>อย่างไรก็ตาม เราต้องใช้เทคโนโลยีอย่างรับผิดชอบและระวังข้อมูลเท็จ</p>''',
                'category': Category.objects.get(name='เทคโนโลยี'),
                'status': 'published'
            },
            {
                'title': 'ความสำคัญของการอนุรักษ์สิ่งแวดล้อมในชุมชน',
                'excerpt': 'การอนุรักษ์สิ่งแวดล้อมในระดับชุมชนเป็นรากฐานสำคัญของการพัฒนาที่ยั่งยืน',
                'content': '''<h2>สิ่งแวดล้อมและชุมชน</h2>
                
                <p>การอนุรักษ์สิ่งแวดล้อมในระดับชุมชนเป็นสิ่งสำคัญที่ทุกคนควรให้ความสนใจ</p>
                
                <h3>วิธีการอนุรักษ์</h3>
                <ul>
                    <li>ลดการใช้พลาสติก</li>
                    <li>คัดแยกขยะ</li>
                    <li>ใช้พลังงานอย่างประหยัด</li>
                    <li>ปลูกต้นไม้ในชุมชน</li>
                </ul>
                
                <p>การเริ่มต้นจากสิ่งเล็กๆ ในชุมชนจะนำไปสู่การเปลี่ยนแปลงที่ยิ่งใหญ่</p>''',
                'category': Category.objects.get(name='สิ่งแวดล้อม'),
                'status': 'published'
            }
        ]

        for post_data in posts_data:
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'author': admin_user,
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'category': post_data['category'],
                    'status': post_data['status'],
                    'published_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'Created post: {post.title}')
                # Add some tags
                if 'เทคโนโลยี' in post.title:
                    post.tags.add('เทคโนโลยี', 'ประชาธิปไตย', 'นวัตกรรม')
                elif 'สิ่งแวดล้อม' in post.title:
                    post.tags.add('สิ่งแวดล้อม', 'อนุรักษ์', 'ชุมชน')
                else:
                    post.tags.add('ข่าวสาร', 'สังคม')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
        )