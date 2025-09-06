#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicblogs.settings')

def main():
    """Create sample blog posts for demonstration"""
    django.setup()
    
    from django.contrib.auth.models import User
    from blog.models import Post, Category
    from django.utils.text import slugify
    
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@civicblogs.com', 'admin123456')
        print("✅ Admin user created")
    
    # Create categories
    categories_data = [
        {'name': 'การเมือง', 'slug': 'politics'},
        {'name': 'สังคม', 'slug': 'society'}, 
        {'name': 'เทคโนโลยี', 'slug': 'technology'},
        {'name': 'สิ่งแวดล้อม', 'slug': 'environment'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'slug': cat_data['slug']}
        )
        if created:
            print(f"✅ Category '{cat_data['name']}' created")
    
    # Create sample posts
    posts_data = [
        {
            'title': 'การพัฒนาระบบประชาธิปไตยไทยในยุคดิจิทัล',
            'content': '''
ในยุคที่เทคโนโลยีดิจิทัลเข้ามามีบทบาทสำคัญในทุกแง่มุมของชีวิต การพัฒนาระบบประชาธิปไตยไทยจึงต้องปรับตัวให้สอดคล้องกับการเปลี่ยนแปลงนี้

## ความท้าทายในยุคดิจิทัล

การเข้าถึงข้อมูลที่รวดเร็วและหลากหลายทำให้ประชาชนมีความรู้และความเข้าใจในประเด็นสาธารณะมากขึ้น แต่ในขณะเดียวกันก็เกิดปัญหาข่าวปลอมและข้อมูลที่ไม่ถูกต้อง

## โอกาสในการพัฒนา

- **E-Government**: การให้บริการภาครัฐผ่านระบบดิจิทัล
- **Digital Participation**: การมีส่วนร่วมทางการเมืองผ่านแพลตฟอร์มออนไลน์
- **Transparency**: ความโปร่งใสในการทำงานของรัฐ

## ข้อเสนอแนะ

1. พัฒนาระบบการศึกษาด้านดิจิทัลลิเทอรซี
2. สร้างกลไกการตรวจสอบข้อมูลที่มีประสิทธิภาพ  
3. เสริมสร้างการมีส่วนร่วมของประชาชนผ่านช่องทางดิจิทัล
            ''',
            'category': 'การเมือง',
            'excerpt': 'การพัฒนาประชาธิปไตยไทยในยุคที่เทคโนโลยีดิจิทัลเข้ามามีบทบาทสำคัญ',
        },
        {
            'title': 'ผลกระทบของการเปลี่ยนแปลงสภาพภูมิอากาศต่อเกษตรกรไทย',
            'content': '''
การเปลี่ยนแปลงสภาพภูมิอากาศส่งผลกระทบอย่างรุนแรงต่อภาคเกษตรกรรมของไทย ซึ่งถือเป็นรากฐานสำคัญของเศรษฐกิจประเทศ

## ผลกระทบที่เกิดขึ้น

### ด้านอากาศและสภาพแวดล้อม
- ฝนตกผิดปกติ ทั้งน้ำท่วมและภัยแล้ง
- อุณหภูมิที่สูงขึ้นส่งผลต่อการเจริญเติบโตของพืช
- การเปลี่ยนแปลงของฤดูกาลทำให้การวางแผนการเกษตรยากขึ้น

### ด้านเศรษฐกิจ
- ผลผลิตลดลง ส่งผลต่อรายได้ของเกษตรกร
- ต้นทุนการผลิตสูงขึ้นเนื่องจากต้องปรับปรุงระบบการเกษตร
- ความเสี่ยงในการลงทุนเพิ่มขึ้น

## แนวทางการปรับตัว

1. **เกษตรอัจฉริยะ**: การใช้เทคโนโลยีช่วยในการเกษตร
2. **พันธุ์พืชที่ทนต่อสภาพอากาศ**: การพัฒนาพันธุ์พืชที่สามารถปรับตัวได้
3. **ระบบชลประทาน**: การจัดการน้ำอย่างมีประสิทธิภาพ
4. **การประกันภัยการเกษตร**: การลดความเสี่ยงให้กับเกษตรกร
            ''',
            'category': 'สิ่งแวดล้อม',
            'excerpt': 'ผลกระทบของการเปลี่ยนแปลงสภาพภูมิอากาศที่ส่งผลต่อเกษตรกรไทยและแนวทางการปรับตัว',
        },
        {
            'title': 'AI และอนาคตของการทำงานในประเทศไทย',
            'content': '''
ปัญญาประดิษฐ์ (AI) กำลังเปลี่ยนแปลงโฉมหน้าของตลาดแรงงานทั่วโลก รวมถึงประเทศไทย

## การเปลี่ยนแปลงที่กำลังเกิดขึ้น

### งานที่ถูกแทนที่
- งานที่มีลักษณะซ้ำๆ และคาดเดาได้
- งานการผลิตในโรงงาน
- งานบริการพื้นฐาน

### งานใหม่ที่เกิดขึ้น
- ผู้เชี่ยวชาญด้าน AI และ Machine Learning
- นักวิเคราะห์ข้อมูล
- ผู้พัฒนาระบบอัตโนมัติ

## ความท้าทายสำหรับแรงงานไทย

1. **Skill Gap**: ช่องว่างทักษะระหว่างที่ตลาดต้องการกับที่แรงงานมี
2. **การปรับตัว**: ความจำเป็นในการเรียนรู้ทักษะใหม่
3. **ความเหลื่อมล้ำ**: การเข้าถึงการศึกษาและการฝึกอบรมที่ไม่เท่าเทียม

## แนวทางการเตรียมความพร้อม

- **การศึกษาต่อเนื่อง**: Lifelong Learning
- **การพัฒนาทักษะดิจิทัล**: Digital Literacy
- **การสร้างระบบสวัสดิการใหม่**: รองรับการเปลี่ยนแปลงของตลาดแรงงาน
            ''',
            'category': 'เทคโนโลยี',
            'excerpt': 'การเปลี่ยนแปลงของตลาดแรงงานไทยในยุค AI และแนวทางการเตรียมความพร้อม',
        }
    ]
    
    admin_user = User.objects.get(username='admin')
    
    for post_data in posts_data:
        category = Category.objects.get(name=post_data['category'])
        
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'slug': slugify(post_data['title']),
                'content': post_data['content'],
                'excerpt': post_data['excerpt'],
                'author': admin_user,
                'category': category,
                'status': 'published'
            }
        )
        
        if created:
            print(f"✅ Post '{post_data['title'][:50]}...' created")
    
    print("🎉 Sample data created successfully!")

if __name__ == '__main__':
    main()