# CivicSpace API Endpoints

**Production Base URL:** `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net`  
**Development Base URL:** `http://127.0.0.1:8000`  
**API Version:** `v1`

## 🔗 API Root
All API endpoints are available under `/api/v1/`

## Categories

### GET /api/v1/categories/
Get all categories with post counts
```json
{
  "count": 8,
  "results": [
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

### GET /api/v1/categories/{slug}/
Get category details by slug

### GET /api/v1/categories/{slug}/posts/
Get all posts in a category
```json
{
  "category": {...},
  "posts": [...]
}
```

## Posts

### GET /api/v1/posts/
Get paginated list of all published posts
- **Query params:** 
  - `page=2` - Pagination (20 posts per page)
  - `search=keyword` - Search in title, content, and category
  - `category=slug` - Filter by category slug
  - `tag=slug` - Filter by tag slug

### GET /api/v1/posts/{slug}/
Get single post by slug (increments view count automatically)
```json
{
  "id": 39,
  "title": "Post Title",
  "slug": "post-slug",
  "content": "<p>HTML content</p>",
  "author": "author@email.com",
  "category": {...},
  "tags": [...],
  "featured_image_url": "https://...",
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

### GET /api/v1/posts/latest/
Get latest posts
- **Query params:** `?limit=10` (default: 10, max: 50)

### GET /api/v1/posts/popular/
Get most popular posts by view count  
- **Query params:** `?limit=10` (default: 10, max: 50)

## Videos

### GET /api/v1/videos/
Get paginated list of all published videos
- **Query params:** 
  - `page=2` - Pagination (20 videos per page)
  - `search=keyword` - Search in title and description
  - `category=slug` - Filter by category slug
  - `tag=slug` - Filter by tag slug

### GET /api/v1/videos/{slug}/
Get single video by slug (increments view count automatically)
```json
{
  "id": 17,
  "title": "นาย วุฒนา วาระเพียง อดีต ผอ.รพ.สต.บ้านทุ่งโหนด นครศรีธรรมราช",
  "slug": "video-20250920031618",
  "description": "งานบุญจะงดงามที่สุดเมื่อปลอดภัย ปลอดเหล้า และปลอดการทะเลาะวิวาท",
  "video_url": "https://www.facebook.com/share/v/1BE8657czE/",
  "author": "evo_reaction@hotmail.com",
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ",
    "post_count": 8
  },
  "tags": [],
  "thumbnail_url": "https://civicblogs12.blob.core.windows.net/media/blog/video_thumbnails/059830ff-ad61-4dd0-95d9-29b39197d17c.jpg",
  "thumbnail_alt": "",
  "created_at": "2025-09-20T10:16:18.859592+07:00",
  "updated_at": "2025-09-20T10:16:18.859619+07:00",
  "view_count": 0,
  "status": "published"
}
```

### GET /api/v1/videos/latest/
Get latest videos
- **Query params:** `?limit=10` (default: 10, max: 50)

### GET /api/v1/videos/popular/
Get most popular videos by view count
- **Query params:** `?limit=10` (default: 10, max: 50)

### GET /api/v1/categories/{slug}/videos/
Get all videos in a category
```json
{
  "category": {...},
  "videos": [...]
}
```

### GET /api/v1/tags/{slug}/videos/
Get all videos with a specific tag
```json
{
  "tag": {...},
  "videos": [...]
}
```

## Tags

### GET /api/v1/tags/
Get all tags

### GET /api/v1/tags/{slug}/posts/
Get all posts with a specific tag
```json
{
  "tag": {...},
  "posts": [...]
}
```

## Response Format

All list endpoints return paginated results:
```json
{
  "count": 30,
  "next": "http://localhost:8000/api/v1/posts/?page=2",
  "previous": null,
  "results": [...]
}
```

## 🚀 Implementation Status

### ✅ Completed Features
- **CORS Configuration**: Enabled for frontend integration
- **Pagination**: 20 items per page for all list endpoints
- **Search Functionality**: Full-text search across posts and videos
- **Filtering**: By category slug and tag slug for both posts and videos
- **Azure Blob Storage**: Image and video thumbnail URLs with CDN support
- **Post Analytics**: Reading time calculation and view count tracking
- **Video Analytics**: View count tracking for videos
- **SEO Support**: Meta descriptions and keywords
- **Auto Excerpts**: Generated from post content
- **Video API Endpoints**: Complete API operations for videos
- **Video Serializers**: JSON serialization for video data
- **Video Search**: Full-text search in video titles and descriptions

### ⚠️ Pending Implementation
- **Mixed Content API**: Combined posts and videos endpoints
- **Authentication**: JWT tokens for admin operations
- **Rate Limiting**: API request throttling
- **Caching**: Redis cache for better performance

## 🛠️ For Next.js Integration

### Required Headers
```javascript
// Recommended headers for API requests
{
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
```

### CORS Settings
- **Allowed Origins**: `civicspace.com`, `localhost:3000`
- **Allowed Methods**: `GET, POST, PUT, DELETE, OPTIONS`
- **Allowed Headers**: `Content-Type, Authorization`

### Example Usage (Next.js)
```javascript
// Fetch posts
const response = await fetch('/api/v1/posts/?limit=10&category=technology');
const data = await response.json();

// Search functionality  
const searchResponse = await fetch('/api/v1/posts/?search=keyword');
const searchData = await searchResponse.json();
```

## 🧪 API Testing

### Development Server
```bash
# Start Django development server
python3 manage.py runserver 127.0.0.1:8000

# Test API endpoints
curl http://127.0.0.1:8000/api/v1/posts/
curl http://127.0.0.1:8000/api/v1/videos/
curl http://127.0.0.1:8000/api/v1/categories/
curl http://127.0.0.1:8000/api/v1/tags/
```

### Example API Calls
```bash
# Get all posts with pagination
curl "http://127.0.0.1:8000/api/v1/posts/?page=1&limit=10"

# Search posts
curl "http://127.0.0.1:8000/api/v1/posts/?search=alcohol"

# Filter by category
curl "http://127.0.0.1:8000/api/v1/posts/?category=research"

# Get latest posts
curl "http://127.0.0.1:8000/api/v1/posts/latest/?limit=5"

# Get popular posts
curl "http://127.0.0.1:8000/api/v1/posts/popular/?limit=5"

# Get all videos with pagination
curl "http://127.0.0.1:8000/api/v1/videos/?page=1&limit=10"

# Search videos
curl "http://127.0.0.1:8000/api/v1/videos/?search=เทคนิค"

# Filter videos by category
curl "http://127.0.0.1:8000/api/v1/videos/?category=nakhonsithammarat"

# Get latest videos
curl "http://127.0.0.1:8000/api/v1/videos/latest/?limit=5"

# Get popular videos
curl "http://127.0.0.1:8000/api/v1/videos/popular/?limit=5"
```

## 📝 Notes for Next.js Development

1. **Base URL Configuration**: Use environment variables for API base URL
2. **Error Handling**: All endpoints return appropriate HTTP status codes
3. **Pagination**: Use `count`, `next`, `previous` fields for pagination UI
4. **Image URLs**: Absolute URLs are provided for all images
5. **SEO Data**: Meta descriptions and keywords available for each post
6. **View Tracking**: GET requests to post detail automatically increment view count

---

**Last Updated**: September 20, 2025  
**API Version**: v1  
**Status**: ✅ Complete for Next.js Integration (Posts + Videos + Categories + Tags)  
**Video Endpoints**: ✅ Fully Implemented and Tested