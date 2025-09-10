# Postman API Testing Examples

## Base URL
```
https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net
```

## 1. GET Categories List
**URL:** `{{base_url}}/api/v1/categories/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

**Expected Response:**
```json
{
    "count": 8,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 8,
            "name": "civicspace",
            "slug": "civicspace",
            "description": "",
            "post_count": 2
        },
        {
            "id": 1,
            "name": "เทคโนโลยี",
            "slug": "technology",
            "description": "ข่าวสารและบทความเกี่ยวกับเทคโนโลยี",
            "post_count": 3
        }
    ]
}
```

## 2. GET Posts List (Paginated)
**URL:** `{{base_url}}/api/v1/posts/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

**Query Parameters (Optional):**
- `page=2` - หน้าที่ต้องการ
- `search=keyword` - ค้นหาในชื่อเรื่องและเนื้อหา
- `category=technology` - กรองตามหมวดหมู่
- `tag=tag-slug` - กรองตามแท็ก

**Example with search:**
`{{base_url}}/api/v1/posts/?search=เทคโนโลยี&page=1`

## 3. GET Latest Posts
**URL:** `{{base_url}}/api/v1/posts/latest/?limit=5`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

**Expected Response:**
```json
[
    {
        "id": 39,
        "title": "z11",
        "slug": "z11",
        "excerpt": "asjdbajsc'aHC[oihw[co'Q",
        "author": "evo_reaction@hotmail.com",
        "category": {
            "id": 8,
            "name": "civicspace",
            "slug": "civicspace",
            "description": "",
            "post_count": 2
        },
        "tags": [],
        "featured_image_url": "https://civicblogs12.blob.core.windows.net/media/blog/featured_images/f39ed437-3b37-4899-9160-8c04d02e4b42.png",
        "created_at": "2025-09-09T15:40:12.220005+07:00",
        "updated_at": "2025-09-09T15:40:12.220033+07:00",
        "view_count": 4,
        "reading_time": 1,
        "status": "published"
    }
]
```

## 4. GET Popular Posts
**URL:** `{{base_url}}/api/v1/posts/popular/?limit=5`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

## 5. GET Single Post by Slug
**URL:** `{{base_url}}/api/v1/posts/z11/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

**Expected Response:**
```json
{
    "id": 39,
    "title": "z11",
    "slug": "z11",
    "content": "<p>asjdbajsc'aHC[oihw[co'Q</p>\r\n\r\n<p><img alt=\"\" src=\"https://civicblogs12.blob.core.windows.net/media/uploads/evo_reaction%40hotmail.com/2025/09/09/boonsart-nakornsri-civicspace-001.webp\" style=\"width: 1920px; height: 1080px;\" /></p>",
    "author": "evo_reaction@hotmail.com",
    "category": {
        "id": 8,
        "name": "civicspace",
        "slug": "civicspace",
        "description": "",
        "post_count": 2
    },
    "tags": [],
    "featured_image_url": "https://civicblogs12.blob.core.windows.net/media/blog/featured_images/f39ed437-3b37-4899-9160-8c04d02e4b42.png",
    "featured_image_alt": "",
    "meta_description": "",
    "meta_keywords": "",
    "created_at": "2025-09-09T15:40:12.220005+07:00",
    "updated_at": "2025-09-09T15:40:12.220033+07:00",
    "view_count": 5,
    "reading_time": 1,
    "status": "published"
}
```

## 6. GET Posts by Category
**URL:** `{{base_url}}/api/v1/categories/civicspace/posts/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

**Expected Response:**
```json
{
    "category": {
        "id": 8,
        "name": "civicspace",
        "slug": "civicspace",
        "description": "",
        "post_count": 2
    },
    "posts": [
        {
            "id": 39,
            "title": "z11",
            "slug": "z11",
            "excerpt": "asjdbajsc'aHC[oihw[co'Q",
            "author": "evo_reaction@hotmail.com",
            "category": {...},
            "tags": [],
            "featured_image_url": "https://civicblogs12.blob.core.windows.net/media/blog/featured_images/f39ed437-3b37-4899-9160-8c04d02e4b42.png",
            "created_at": "2025-09-09T15:40:12.220005+07:00",
            "updated_at": "2025-09-09T15:40:12.220033+07:00",
            "view_count": 5,
            "reading_time": 1,
            "status": "published"
        }
    ]
}
```

## 7. GET Category Detail
**URL:** `{{base_url}}/api/v1/categories/technology/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

## 8. GET All Tags
**URL:** `{{base_url}}/api/v1/tags/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

## 9. GET Posts by Tag
**URL:** `{{base_url}}/api/v1/tags/{tag-slug}/posts/`
**Method:** GET
**Headers:**
```
Accept: application/json
Content-Type: application/json
```

---

## Postman Environment Variables
สร้าง Environment ใน Postman และเพิ่มตัวแปร:

**Variable Name:** `base_url`
**Initial Value:** `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net`
**Current Value:** `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net`

หรือสำหรับทดสอบ local:
**Variable Name:** `base_url`  
**Initial Value:** `http://localhost:8000`
**Current Value:** `http://localhost:8000`

## Common HTTP Status Codes
- `200 OK` - สำเร็จ
- `404 Not Found` - ไม่พบข้อมูล (post slug, category slug ไม่ถูกต้อง)
- `500 Internal Server Error` - ข้อผิดพลาดเซิร์ฟเวอร์

## Notes
- ทุก endpoint รองรับ CORS สำหรับ civicspace.com
- รูปภาพจาก Azure Blob Storage จะมี URL แบบ https://civicblogs12.blob.core.windows.net/media/...
- การเรียก POST detail จะเพิ่ม view_count อัตโนมัติ
- Pagination ค่าเริ่มต้น 20 รายการต่อหน้า