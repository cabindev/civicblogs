# CivicSpace API Endpoints

Base URL: `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net`

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
- Query params: `?page=2&search=keyword&category=slug&tag=slug`

### GET /api/v1/posts/{slug}/
Get single post by slug (increments view count)
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
- Query params: `?limit=10` (default: 10)

### GET /api/v1/posts/popular/
Get most popular posts by view count  
- Query params: `?limit=10` (default: 10)

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

## Features

- ✅ CORS enabled for civicspace.com
- ✅ Pagination (20 items per page)
- ✅ Search functionality  
- ✅ Category and tag filtering
- ✅ Azure Blob Storage image URLs
- ✅ Reading time calculation
- ✅ View count tracking
- ✅ Auto-generated excerpts
- ✅ SEO meta fields