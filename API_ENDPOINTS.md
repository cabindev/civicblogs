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
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "name": "เดือนสิบเมืองคอน",
      "slug": "nakhonsithammarat",
      "description": "งานบุญเดือนสิบ",
      "post_count": 9
    },
    {
      "id": 11,
      "name": "บวชสร้างสุข วิถีอ่างทอง",
      "slug": "ordain",
      "description": "งานบวชในพื้นที่จังหวัดอ่างทอง",
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
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ"
  },
  "posts": [
    {
      "id": 51,
      "title": "ประเพณีชิงเปรต",
      "slug": "post-new",
      "excerpt": "สังคมไทยมีความใกล้ชิดกับเปรตมายาวนาน โดยเฉพาะภาคใต้ของไทย...",
      "featured_image_url": "https://civicblogs12.blob.core.windows.net/media/blog/featured_images/0df23d0e-a055-4ac5-8138-24e600d72d94.jpg"
    }
  ]
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
  "id": 51,
  "title": "ประเพณีชิงเปรต",
  "slug": "post-new",
  "content": "<p>สังคมไทยมีความใกล้ชิดกับเปรตมายาวนาน โดยเฉพาะภาคใต้ของไทย ที่ยังมีความเชื่อความข้องเกี่ยวกับวัฒนธรรมประเพณีท้องถิ่น เช่น ประเพณีชิงเปรต...</p>",
  "author": "evo_reaction@hotmail.com",
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ",
    "post_count": 9
  },
  "post_type": {
    "id": 5,
    "name": "Article",
    "slug": "article",
    "description": "บทความและเนื้อหาเชิงลึก",
    "icon": "📝",
    "color": "#8B5CF6",
    "post_count": 5
  },
  "tags": [
    {
      "id": 9,
      "name": "งานบุญเดือนสิบ",
      "slug": "งานบญเดอนสบ"
    },
    {
      "id": 10,
      "name": "เดือนสิบเมืองคอน",
      "slug": "เดอนสบเมองคอน"
    }
  ],
  "featured_image_url": "https://civicblogs12.blob.core.windows.net/media/blog/featured_images/0df23d0e-a055-4ac5-8138-24e600d72d94.jpg",
  "created_at": "2025-09-30T15:34:23.624596+07:00",
  "updated_at": "2025-09-30T15:56:39.864585+07:00",
  "view_count": 0,
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
  "description": "\"การเปลี่ยนแปลงไม่ได้เกิดขึ้นในวันเดียว แต่เพราะเราเคยลุกขึ้นรณรงค์ จากงานบุญที่เต็มไปด้วยเหล้าและความเสี่ยง วันนี้งานบุญเดือนสิบได้พิสูจน์แล้วว่า งานบุญจะงดงามที่สุดเมื่อปลอดภัย ปลอดเหล้า และปลอดการทะเลาะวิวาท\"",
  "video_url": "https://www.facebook.com/share/v/1BE8657czE/",
  "author": "evo_reaction@hotmail.com",
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ",
    "post_count": 9
  },
  "tags": [],
  "thumbnail_url": "https://civicblogs12.blob.core.windows.net/media/blog/video_thumbnails/059830ff-ad61-4dd0-95d9-29b39197d17c.jpg",
  "thumbnail_alt": "",
  "created_at": "2025-09-20T10:16:18.859592+07:00",
  "updated_at": "2025-09-20T10:16:18.859619+07:00",
  "view_count": 1,
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
  "category": {
    "id": 10,
    "name": "เดือนสิบเมืองคอน",
    "slug": "nakhonsithammarat",
    "description": "งานบุญเดือนสิบ"
  },
  "videos": [
    {
      "id": 17,
      "title": "นาย วุฒนา วาระเพียง อดีต ผอ.รพ.สต.บ้านทุ่งโหนด นครศรีธรรมราช",
      "slug": "video-20250920031618",
      "video_url": "https://www.facebook.com/share/v/1BE8657czE/",
      "thumbnail_url": "https://civicblogs12.blob.core.windows.net/media/blog/video_thumbnails/059830ff-ad61-4dd0-95d9-29b39197d17c.jpg"
    }
  ]
}
```

### GET /api/v1/tags/{slug}/videos/
Get all videos with a specific tag
```json
{
  "tag": {
    "id": 9,
    "name": "งานบุญเดือนสิบ",
    "slug": "งานบญเดอนสบ"
  },
  "videos": [
    {
      "id": 17,
      "title": "นาย วุฒนา วาระเพียง อดีต ผอ.รพ.สต.บ้านทุ่งโหนด นครศรีธรรมราช",
      "slug": "video-20250920031618",
      "video_url": "https://www.facebook.com/share/v/1BE8657czE/",
      "view_count": 1
    }
  ]
}
```

## Tags

### GET /api/v1/tags/
Get all tags

### GET /api/v1/tags/{slug}/posts/
Get all posts with a specific tag
```json
{
  "tag": {
    "id": 9,
    "name": "งานบุญเดือนสิบ",
    "slug": "งานบญเดอนสบ"
  },
  "posts": [
    {
      "id": 51,
      "title": "ประเพณีชิงเปรต",
      "slug": "post-new",
      "excerpt": "สังคมไทยมีความใกล้ชิดกับเปรตมายาวนาน โดยเฉพาะภาคใต้ของไทย...",
      "view_count": 0,
      "reading_time": 1
    }
  ]
}
```

## Response Format

All list endpoints return paginated results:
```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 51,
      "title": "ประเพณีชิงเปรต",
      "slug": "post-new",
      "excerpt": "สังคมไทยมีความใกล้ชิดกับเปรตมายาวนาน...",
      "author": "evo_reaction@hotmail.com",
      "category": {
        "id": 10,
        "name": "เดือนสิบเมืองคอน",
        "slug": "nakhonsithammarat"
      },
      "featured_image_url": "https://civicblogs12.blob.core.windows.net/media/blog/featured_images/0df23d0e-a055-4ac5-8138-24e600d72d94.jpg",
      "created_at": "2025-09-30T15:34:23.624596+07:00",
      "view_count": 0,
      "reading_time": 1,
      "status": "published"
    }
  ]
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
- **Allowed Origins**: `civicspace.com`, `localhost:3000`, `localhost:3001`
- **Allowed Methods**: `GET, POST, PUT, DELETE, OPTIONS`
- **Allowed Headers**: `Content-Type, Authorization, X-Requested-With`

### Base URL Configuration
```javascript
// .env.local (Next.js)
NEXT_PUBLIC_API_BASE_URL=https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net
NEXT_PUBLIC_API_VERSION=v1

// Development
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### API Service (Next.js)
```javascript
// lib/api.js
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
const API_VERSION = process.env.NEXT_PUBLIC_API_VERSION || 'v1';

export class CivicBlogsAPI {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api/${API_VERSION}`;
  }

  // Posts API
  async getPosts(params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(`${this.baseURL}/posts/?${searchParams}`);
    return response.json();
  }

  async getPost(slug) {
    const response = await fetch(`${this.baseURL}/posts/${slug}/`);
    return response.json();
  }

  async getLatestPosts(limit = 10) {
    const response = await fetch(`${this.baseURL}/posts/latest/?limit=${limit}`);
    return response.json();
  }

  async getPopularPosts(limit = 10) {
    const response = await fetch(`${this.baseURL}/posts/popular/?limit=${limit}`);
    return response.json();
  }

  // Videos API
  async getVideos(params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(`${this.baseURL}/videos/?${searchParams}`);
    return response.json();
  }

  async getVideo(slug) {
    const response = await fetch(`${this.baseURL}/videos/${slug}/`);
    return response.json();
  }

  async getLatestVideos(limit = 10) {
    const response = await fetch(`${this.baseURL}/videos/latest/?limit=${limit}`);
    return response.json();
  }

  async getPopularVideos(limit = 10) {
    const response = await fetch(`${this.baseURL}/videos/popular/?limit=${limit}`);
    return response.json();
  }

  // Categories API
  async getCategories() {
    const response = await fetch(`${this.baseURL}/categories/`);
    return response.json();
  }

  async getCategory(slug) {
    const response = await fetch(`${this.baseURL}/categories/${slug}/`);
    return response.json();
  }

  async getCategoryPosts(slug, params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(`${this.baseURL}/categories/${slug}/posts/?${searchParams}`);
    return response.json();
  }

  async getCategoryVideos(slug, params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(`${this.baseURL}/categories/${slug}/videos/?${searchParams}`);
    return response.json();
  }

  // Tags API
  async getTags() {
    const response = await fetch(`${this.baseURL}/tags/`);
    return response.json();
  }

  async getTagPosts(slug, params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(`${this.baseURL}/tags/${slug}/posts/?${searchParams}`);
    return response.json();
  }

  async getTagVideos(slug, params = {}) {
    const searchParams = new URLSearchParams(params);
    const response = await fetch(`${this.baseURL}/tags/${slug}/videos/?${searchParams}`);
    return response.json();
  }

  // Search API
  async search(query, type = 'posts', params = {}) {
    const searchParams = new URLSearchParams({ search: query, ...params });
    const response = await fetch(`${this.baseURL}/${type}/?${searchParams}`);
    return response.json();
  }
}

// Export singleton instance
export const civicBlogsAPI = new CivicBlogsAPI();
```

### Usage (Next.js Pages/Components)
```javascript
import { civicBlogsAPI } from '../lib/api';

// In a page component
export async function getStaticProps() {
  try {
    const postsData = await civicBlogsAPI.getLatestPosts(10);
    const videosData = await civicBlogsAPI.getLatestVideos(5);
    const categories = await civicBlogsAPI.getCategories();

    return {
      props: {
        posts: postsData.results || [],
        videos: videosData.results || [],
        categories: categories.results || []
      },
      revalidate: 300 // Revalidate every 5 minutes
    };
  } catch (error) {
    console.error('API Error:', error);
    return {
      props: { posts: [], videos: [], categories: [] }
    };
  }
}

// In a dynamic page [slug].js
export async function getStaticPaths() {
  const postsData = await civicBlogsAPI.getPosts({ limit: 100 });
  const paths = postsData.results.map((post) => ({
    params: { slug: post.slug }
  }));

  return { paths, fallback: 'blocking' };
}

export async function getStaticProps({ params }) {
  try {
    const post = await civicBlogsAPI.getPost(params.slug);
    const relatedPosts = await civicBlogsAPI.getCategoryPosts(
      post.category.slug, 
      { limit: 3 }
    );

    return {
      props: { post, relatedPosts: relatedPosts.posts || [] },
      revalidate: 60
    };
  } catch (error) {
    return { notFound: true };
  }
}

// In a search component
import { useState, useEffect } from 'react';

export function SearchComponent() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (searchQuery) => {
    if (!searchQuery) return;
    
    setLoading(true);
    try {
      const [postsResult, videosResult] = await Promise.all([
        civicBlogsAPI.search(searchQuery, 'posts'),
        civicBlogsAPI.search(searchQuery, 'videos')
      ]);
      
      setResults([
        ...postsResult.results.map(item => ({ ...item, type: 'post' })),
        ...videosResult.results.map(item => ({ ...item, type: 'video' }))
      ]);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSearch(query)}
        placeholder="ค้นหาบทความและวิดีโอ..."
      />
      {loading && <p>กำลังค้นหา...</p>}
      {results.map(item => (
        <div key={`${item.type}-${item.id}`}>
          <h3>{item.title}</h3>
          <p>{item.type === 'post' ? 'บทความ' : 'วิดีโอ'}</p>
        </div>
      ))}
    </div>
  );
}
```

## 🧪 API Testing

### 🔗 **Quick Test Links**

#### 🌐 **Production API (Live)**
- **All Posts:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/
- **Latest Posts:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/latest/?limit=5
- **Popular Posts:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/popular/?limit=5
- **Single Post:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/post-new/
- **All Videos:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/videos/
- **Latest Videos:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/videos/latest/?limit=5
- **All Categories:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/categories/
- **Category Posts:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/categories/nakhonsithammarat/posts/
- **Category Videos:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/categories/nakhonsithammarat/videos/
- **All Tags:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/tags/
- **Search Posts:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/?search=เดือนสิบ
- **Search Videos:** https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/videos/?search=งานบุญ

#### 🛠️ **Development Server**
```bash
# Start Django development server
python3 manage.py runserver 127.0.0.1:8000

# Test API endpoints
curl http://127.0.0.1:8000/api/v1/posts/
curl http://127.0.0.1:8000/api/v1/videos/
curl http://127.0.0.1:8000/api/v1/categories/
curl http://127.0.0.1:8000/api/v1/tags/
```

### API Calls
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

### 💡 **Testing Methods:**

**1. Browser** - Click any production URL above to view JSON responses directly
**2. curl Command:**
```bash
curl "https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/"
```

**3. Postman/Insomnia** - Import any of the production URLs
**4. JavaScript fetch:**
```javascript
fetch('https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/posts/')
  .then(response => response.json())
  .then(data => console.log(data));
```

**5. Next.js Integration:**
```javascript
import { civicBlogsAPI } from '../lib/api';

// Get latest posts
const posts = await civicBlogsAPI.getLatestPosts(10);
console.log(posts);
```

## 📝 Notes for Next.js Development

### 🚀 Ready-to-Use Features
1. **Complete API Service Class**: Copy-paste ready `CivicBlogsAPI` class
2. **Environment Configuration**: Production and development URLs provided
3. **Error Handling**: Try-catch blocks in all code samples
4. **TypeScript Support**: Add type definitions as needed
5. **Static Site Generation**: Implementation for `getStaticProps` and `getStaticPaths`
6. **Search Functionality**: Combined posts and videos search implementation
7. **Pagination Support**: Built-in pagination handling
8. **View Tracking**: Automatic view count increment on detail pages

### 🔗 Integration Checklist
- [ ] Copy `CivicBlogsAPI` class to `lib/api.js`
- [ ] Set up environment variables in `.env.local`
- [ ] Test API connection with development server
- [ ] Implement error boundaries for API failures
- [ ] Add loading states for better UX
- [ ] Configure CORS if needed
- [ ] Set up image optimization for Next.js
- [ ] Add TypeScript interfaces (optional)

### 🎯 Performance Recommendations
- Use `getStaticProps` with `revalidate` for better performance
- Implement caching for frequently accessed data
- Use `getStaticPaths` with `fallback: 'blocking'` for dynamic routes
- Consider implementing infinite scroll for long lists
- Add image optimization with Next.js Image component

### 🔧 Error Handling
```javascript
// Add to your API service for better error handling
async handleResponse(response) {
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

// Use in all API methods
async getPosts(params = {}) {
  const searchParams = new URLSearchParams(params);
  const response = await fetch(`${this.baseURL}/posts/?${searchParams}`);
  return this.handleResponse(response);
}
```

---

---

**Last Updated**: October 2, 2025  
**API Version**: v1  
**Status**: ✅ Complete for Next.js Integration (Posts + Videos + Categories + Tags)  
**Next.js Ready**: ✅ Complete API Service Class with Real Data  
**Production URL**: https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net  
**Real Data**: ✅ All responses use actual production data  

## 📊 Current Data Summary
- **Categories**: 2 active categories (เดือนสิบเมืองคอน, บวชสร้างสุข วิถีอ่างทอง)
- **Posts**: 12 published posts with rich content
- **Videos**: 11 published videos with Facebook integration
- **Post Types**: 6 types (Infographic, Article, Facebook Post, etc.)
- **Tags**: Active tagging system with Thai language support
- **Media**: Azure Blob Storage integration for images and thumbnails