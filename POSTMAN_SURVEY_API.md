# 📬 Postman Testing Guide - Survey API

## 🔗 Base URLs
- **Development**: `http://127.0.0.1:8000`
- **Production**: `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net`

---

## 📋 Survey API Endpoints

### 1️⃣ GET All Surveys
**URL**: `http://127.0.0.1:8000/api/v1/surveys/`

**Method**: `GET`

**Headers**:
```
Content-Type: application/json
Accept: application/json
```

**Response** (200 OK):
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "title": "สำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ",
      "slug": "survey-20251008044448",
      "description": "แบบสอบถามสำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ และงานกาชาดปี 2568",
      "author": "evo_reaction@hotmail.com",
      "category": {
        "id": 10,
        "name": "เดือนสิบเมืองคอน",
        "slug": "nakhonsithammarat",
        "description": "งานบุญเดือนสิบ",
        "post_count": 12
      },
      "survey_file_url": "https://civicblogs12.blob.core.windows.net/media/surveys/files/b72e3bb5-b1a8-41b0-9872-86b8fb98605b.docx",
      "is_published": true,
      "survey_date": "2025-09-22",
      "response_count": 0,
      "view_count": 0,
      "created_at": "2025-10-08T11:44:48.202564+07:00",
      "updated_at": "2025-10-08T11:44:48.202601+07:00",
      "published_at": "2025-10-08T11:44:48.082104+07:00"
    }
  ]
}
```

---

### 2️⃣ GET Survey Detail
**URL**: `http://127.0.0.1:8000/api/v1/surveys/survey-20251008044448/`

**Method**: `GET`

**Headers**:
```
Content-Type: application/json
Accept: application/json
```

**Response** (200 OK):
```json
{
  "id": 2,
  "title": "สำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ",
  "slug": "survey-20251008044448",
  "description": "แบบสอบถามสำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ และงานกาชาดปี 2568",
  "author": "evo_reaction@hotmail.com",
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ",
    "post_count": 12
  },
  "survey_file_url": "https://civicblogs12.blob.core.windows.net/media/surveys/files/b72e3bb5-b1a8-41b0-9872-86b8fb98605b.docx",
  "is_published": true,
  "survey_date": "2025-09-22",
  "response_count": 0,
  "view_count": 1,
  "created_at": "2025-10-08T11:44:48.202564+07:00",
  "updated_at": "2025-10-08T11:44:48.202601+07:00",
  "published_at": "2025-10-08T11:44:48.082104+07:00",
  "responses": {
    "total": 0,
    "verified": 0,
    "complete": 0
  }
}
```

**Note**: `view_count` จะเพิ่มขึ้นทุกครั้งที่เรียก endpoint นี้

---

### 3️⃣ GET Latest Surveys
**URL**: `http://127.0.0.1:8000/api/v1/surveys/latest/?limit=5`

**Method**: `GET`

**Query Parameters**:
- `limit` (optional): จำนวนผลลัพธ์ (default: 10, max: 50)

**Example URLs**:
```
http://127.0.0.1:8000/api/v1/surveys/latest/
http://127.0.0.1:8000/api/v1/surveys/latest/?limit=3
http://127.0.0.1:8000/api/v1/surveys/latest/?limit=10
```

---

### 4️⃣ GET Popular Surveys
**URL**: `http://127.0.0.1:8000/api/v1/surveys/popular/?limit=5`

**Method**: `GET`

**Query Parameters**:
- `limit` (optional): จำนวนผลลัพธ์ (default: 10, max: 50)

**Example URLs**:
```
http://127.0.0.1:8000/api/v1/surveys/popular/
http://127.0.0.1:8000/api/v1/surveys/popular/?limit=3
```

---

### 5️⃣ GET Surveys by Category
**URL**: `http://127.0.0.1:8000/api/v1/categories/nakhonsithammarat/surveys/`

**Method**: `GET`

**Response** (200 OK):
```json
{
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ",
    "post_count": 12
  },
  "surveys": [
    {
      "id": 2,
      "title": "สำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ",
      "slug": "survey-20251008044448",
      "description": "แบบสอบถามสำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ และงานกาชาดปี 2568",
      "author": "evo_reaction@hotmail.com",
      "category": {
        "id": 10,
        "name": "เดือนสิบเมืองคอน",
        "slug": "nakhonsithammarat",
        "description": "งานบุญเดือนสิบ",
        "post_count": 12
      },
      "survey_file_url": "https://civicblogs12.blob.core.windows.net/media/surveys/files/b72e3bb5-b1a8-41b0-9872-86b8fb98605b.docx",
      "is_published": true,
      "survey_date": "2025-09-22",
      "response_count": 0,
      "view_count": 1,
      "created_at": "2025-10-08T11:44:48.202564+07:00",
      "updated_at": "2025-10-08T11:44:48.202601+07:00",
      "published_at": "2025-10-08T11:44:48.082104+07:00"
    }
  ]
}
```

**Example Category Slugs**:
- `nakhonsithammarat` - เดือนสิบเมืองคอน
- `ordain` - บวชสร้างสุข วิถีอ่างทอง

---

### 6️⃣ Search Surveys
**URL**: `http://127.0.0.1:8000/api/v1/surveys/?search=เดือนสิบ`

**Method**: `GET`

**Query Parameters**:
- `search`: คำค้นหาใน title, description, category

**Example URLs**:
```
http://127.0.0.1:8000/api/v1/surveys/?search=เดือนสิบ
http://127.0.0.1:8000/api/v1/surveys/?search=บวช
http://127.0.0.1:8000/api/v1/surveys/?search=งานบุญ
```

---

### 7️⃣ Filter by Category
**URL**: `http://127.0.0.1:8000/api/v1/surveys/?category=nakhonsithammarat`

**Method**: `GET`

**Query Parameters**:
- `category`: category slug

**Example URLs**:
```
http://127.0.0.1:8000/api/v1/surveys/?category=nakhonsithammarat
http://127.0.0.1:8000/api/v1/surveys/?category=ordain
```

---

## 🧪 Postman Collection Setup

### Import into Postman:

1. **Create New Collection**: "CivicSpace Survey API"

2. **Add Environment Variables**:
   - Variable: `base_url`
   - Development: `http://127.0.0.1:8000`
   - Production: `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net`

3. **Request Template**:
   ```
   GET {{base_url}}/api/v1/surveys/

   Headers:
   Content-Type: application/json
   Accept: application/json
   ```

---

## 📊 Test Data

### Available Surveys:
1. **ID: 2** - สำรวจความคิดเห็นต่อการจัดงานประเพณีสารทเดือนสิบ
   - Slug: `survey-20251008044448`
   - Category: `nakhonsithammarat`
   - File: Word Document (.docx)

2. **ID: 1** - แบบสำรวจข้อมูลการจัดงานบุญประเพณี และงานบวชนาค
   - Slug: `survey-20251008044344`
   - Category: `ordain`
   - File: Word Document (.docx)

---

## ✅ Expected Status Codes

- **200 OK**: Request successful
- **404 Not Found**: Survey not found (wrong slug)
- **500 Internal Server Error**: Server error

---

## 🔧 Quick Test Commands (cURL)

```bash
# 1. All Surveys
curl -X GET "http://127.0.0.1:8000/api/v1/surveys/" \
  -H "Content-Type: application/json"

# 2. Survey Detail
curl -X GET "http://127.0.0.1:8000/api/v1/surveys/survey-20251008044448/" \
  -H "Content-Type: application/json"

# 3. Latest Surveys
curl -X GET "http://127.0.0.1:8000/api/v1/surveys/latest/?limit=5" \
  -H "Content-Type: application/json"

# 4. Popular Surveys
curl -X GET "http://127.0.0.1:8000/api/v1/surveys/popular/?limit=5" \
  -H "Content-Type: application/json"

# 5. Surveys by Category
curl -X GET "http://127.0.0.1:8000/api/v1/categories/nakhonsithammarat/surveys/" \
  -H "Content-Type: application/json"

# 6. Search
curl -X GET "http://127.0.0.1:8000/api/v1/surveys/?search=เดือนสิบ" \
  -H "Content-Type: application/json"

# 7. Filter by Category
curl -X GET "http://127.0.0.1:8000/api/v1/surveys/?category=nakhonsithammarat" \
  -H "Content-Type: application/json"
```

---

## 📝 Response Fields Explained

### Survey List Response:
- `id`: Survey ID
- `title`: ชื่อแบบสำรวจ
- `slug`: URL-friendly identifier
- `description`: คำอธิบาย
- `author`: ผู้สร้าง
- `category`: หมวดหมู่ (object)
- `survey_file_url`: URL ไฟล์ Word/Excel (Azure Blob Storage)
- `is_published`: เผยแพร่หรือไม่ (true/false)
- `survey_date`: วันที่สำรวจ (YYYY-MM-DD)
- `response_count`: จำนวนคำตอบ
- `view_count`: จำนวนครั้งที่เข้าชม
- `created_at`: วันที่สร้าง (ISO 8601)
- `updated_at`: วันที่อัปเดตล่าสุด
- `published_at`: วันที่เผยแพร่

### Survey Detail Response (Additional Fields):
- `responses`: สถิติคำตอบ
  - `total`: จำนวนคำตอบทั้งหมด
  - `verified`: จำนวนคำตอบที่ตรวจสอบแล้ว
  - `complete`: จำนวนคำตอบที่กรอกครบ

---

## 🚀 Production Testing

Replace `http://127.0.0.1:8000` with production URL:
```
https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/surveys/
```

---

**Last Updated**: October 8, 2025
**API Version**: v1
**Server**: Django 5.2.5 + DRF
**Database**: Supabase PostgreSQL
**Storage**: Azure Blob Storage
