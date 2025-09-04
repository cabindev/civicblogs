# CivicBlogs

แพลตฟอร์มบล็อกสำหรับการแสดงความคิดเห็นและการสื่อสารของประชาชน

## คุณสมบัติหลัก

- ✅ ระบบเขียนบล็อกพร้อม Rich Text Editor (CKEditor)
- ✅ ระบบจัดการรูปภาพและการอัปโหลดไฟล์
- ✅ ระบบหมวดหมู่และแท็ก
- ✅ ระบบความคิดเห็น
- ✅ ระบบสมัครสมาชิกรับข้อมูลข่าวสาร
- ✅ ระบบค้นหา
- ✅ Responsive Design พร้อม Bootstrap 5
- ✅ SEO Friendly URLs
- ✅ การจัดการผู้ใช้งาน
- ✅ Admin Panel ที่ครบครันสำหรับการจัดการ

## เทคโนโลยีที่ใช้

- **Backend**: Django 5.2+
- **Database**: SQLite (development), สามารถเปลี่ยนเป็น PostgreSQL สำหรับ production
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Rich Text Editor**: CKEditor 4
- **Image Processing**: Pillow
- **Tags**: Django-taggit
- **Cloud Storage**: Supabase (configured)

## การติดตั้งและใช้งาน

### ข้อกำหนดระบบ
- Python 3.8+
- pip

### ขั้นตอนการติดตั้ง

1. **Clone repository**
```bash
git clone <repository-url>
cd civicblogs
```

2. **สร้าง virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # สำหรับ Linux/Mac
# หรือ
venv\Scripts\activate  # สำหรับ Windows
```

3. **ติดตั้ง dependencies**
```bash
pip install -r requirements.txt
```

4. **ตั้งค่า environment variables**
สร้างไฟล์ `.env` และเพิ่มข้อมูล:
```env
DEBUG=True
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **สร้าง superuser**
```bash
python manage.py createsuperuser
```
หรือใช้ข้อมูลที่มีอยู่:
- Email: evo_reaction@hotmail.com
- Password: YY_12345

7. **เพิ่มข้อมูลตัวอย่าง (ไม่บังคับ)**
```bash
python manage.py populate_sample_data
```

8. **เริ่มเซิร์ฟเวอร์**
```bash
python manage.py runserver
```

เว็บไซต์จะพร้อมใช้งานที่ `http://localhost:8000`

## การใช้งาน

### Admin Panel
เข้าถึงได้ที่ `http://localhost:8000/admin/`
- จัดการบทความ, หมวดหมู่, แท็ก
- อนุมัติความคิดเห็น
- จัดการผู้สมัครรับข้อมูลข่าวสาร
- ดูข้อความติดต่อ

### CKEditor สำหรับการอัปโหลดรูปภาพ
- เข้าถึงได้ผ่าน admin panel
- รองรับการอัปโหลดและจัดการรูปภาพ
- ปรับขนาดรูปภาพอัตโนมัติเพื่อประหยัดพื้นที่

### API Endpoints
- `/` - หน้าแรก
- `/post/<slug>/` - หน้าบทความ
- `/category/<slug>/` - หน้าหมวดหมู่
- `/tag/<slug>/` - หน้าแท็ก
- `/search/` - หน้าค้นหา
- `/contact/` - หน้าติดต่อ
- `/about/` - หน้าเกี่ยวกับเรา

## โครงสร้างโปรเจค

```
civicblogs/
├── civicblogs/          # Django project settings
├── blog/                # Main blog application
│   ├── models.py       # Database models
│   ├── views.py        # View logic
│   ├── admin.py        # Admin configuration
│   ├── forms.py        # Forms
│   └── urls.py         # URL routing
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   └── blog/           # Blog templates
├── static/              # Static files (CSS, JS)
├── media/               # User uploaded files
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
└── manage.py           # Django management script
```

## การปรับแต่งและ Scalability

### Database
- ปัจจุบันใช้ SQLite สำหรับ development
- สำหรับ production แนะนำให้เปลี่ยนเป็น PostgreSQL
- รองรับ Supabase PostgreSQL

### Media Storage
- ปัจจุบันเก็บไฟล์ในระบบไฟล์
- สามารถเปลี่ยนไปใช้ Cloud Storage (AWS S3, Google Cloud, etc.)
- ตั้งค่า Django Storages ไว้แล้ว

### Performance
- ใช้ Database indexes สำหรับการค้นหาที่รวดเร็ว
- Query optimization ด้วย select_related และ prefetch_related
- Image optimization อัตโนมัติ

### Security
- CSRF protection
- SQL injection protection
- Input validation และ sanitization
- Comment moderation

## การพัฒนาต่อ

### เพิ่มฟีเจอร์ใหม่
1. ระบบสมาชิก (User registration)
2. ระบบโหวตบทความ
3. ระบบแชร์บทความ
4. การแจ้งเตือนทาง Email
5. Multi-language support
6. Analytics และ reporting

### การปรับปรุงเพิ่มเติม
1. เปลี่ยนจาก CKEditor 4 เป็น CKEditor 5
2. เพิ่ม Progressive Web App (PWA) support
3. ระบบ caching
4. Full-text search ด้วย Elasticsearch

## การสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ:
- Email: evo_reaction@hotmail.com
- สร้าง issue ใน repository

## License

This project is open source and available under the [MIT License](LICENSE).

---

พัฒนาโดย CivicBlogs Team 🚀# civicblogs
