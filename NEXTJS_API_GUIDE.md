# Next.js Integration Guide - CivicBlogs API

## API Base URL

**Production**: `https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1`

## Category API Endpoint

### Get All Categories

```typescript
// Endpoint
GET /api/v1/categories/

// Response
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 14,
      "name": "กระทงสาย",
      "slug": "loikrathongsai",
      "description": "ลอยกระทงสายจังหวัดตาก",
      "post_count": 0,
      "video_count": 5,      // NEW!
      "survey_count": 2,     // NEW!
      "total_count": 7       // NEW!
    }
  ]
}
```

## Next.js TypeScript Types

### 1. สร้าง Types

```typescript
// types/api.ts

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  post_count: number;
  video_count: number;
  survey_count: number;
  total_count: number;
}

export interface CategoryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Category[];
}
```

### 2. Fetch Categories

```typescript
// lib/api.ts

const API_BASE_URL = 'https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1';

export async function getCategories(): Promise<Category[]> {
  const response = await fetch(`${API_BASE_URL}/categories/`, {
    next: { revalidate: 3600 } // Cache for 1 hour
  });

  if (!response.ok) {
    throw new Error('Failed to fetch categories');
  }

  const data: CategoryResponse = await response.json();
  return data.results;
}
```

### 3. Display Categories Component

```typescript
// components/CategoryList.tsx

import { getCategories } from '@/lib/api';
import type { Category } from '@/types/api';

export default async function CategoryList() {
  const categories = await getCategories();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {categories.map((category) => (
        <CategoryCard key={category.id} category={category} />
      ))}
    </div>
  );
}

function CategoryCard({ category }: { category: Category }) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
      <h3 className="text-xl font-bold mb-2">{category.name}</h3>
      <p className="text-gray-600 mb-4">{category.description}</p>

      <div className="grid grid-cols-3 gap-4 text-center">
        {/* Posts */}
        <div className="bg-blue-50 rounded-lg p-3">
          <div className="text-2xl font-bold text-blue-600">
            {category.post_count}
          </div>
          <div className="text-xs text-gray-600">Posts</div>
        </div>

        {/* Videos */}
        <div className="bg-red-50 rounded-lg p-3">
          <div className="text-2xl font-bold text-red-600">
            {category.video_count}
          </div>
          <div className="text-xs text-gray-600">Videos</div>
        </div>

        {/* Surveys */}
        <div className="bg-green-50 rounded-lg p-3">
          <div className="text-2xl font-bold text-green-600">
            {category.survey_count}
          </div>
          <div className="text-xs text-gray-600">Surveys</div>
        </div>
      </div>

      <div className="mt-4 text-center">
        <div className="text-sm text-gray-500">
          Total Content: <span className="font-bold">{category.total_count}</span>
        </div>
      </div>
    </div>
  );
}
```

## Client-Side Fetching (Alternative)

```typescript
// app/categories/page.tsx

'use client';

import { useState, useEffect } from 'react';
import type { Category } from '@/types/api';

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/api/v1/categories/')
      .then(res => res.json())
      .then(data => {
        setCategories(data.results);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {categories.map(category => (
        <div key={category.id}>
          <h2>{category.name}</h2>
          <p>Posts: {category.post_count}</p>
          <p>Videos: {category.video_count}</p>
          <p>Surveys: {category.survey_count}</p>
          <p>Total: {category.total_count}</p>
        </div>
      ))}
    </div>
  );
}
```

## All Available Endpoints

### Categories
- `GET /api/v1/categories/` - List all categories with counts
- `GET /api/v1/categories/{slug}/` - Get category details

### Posts
- `GET /api/v1/posts/` - List all published posts
- `GET /api/v1/posts/{slug}/` - Get post details
- `GET /api/v1/posts/latest/` - Get latest posts
- `GET /api/v1/posts/popular/` - Get popular posts
- `GET /api/v1/posts/category/{category_slug}/` - Posts by category

### Videos
- `GET /api/v1/videos/` - List all published videos
- `GET /api/v1/videos/{slug}/` - Get video details
- `GET /api/v1/videos/latest/` - Get latest videos
- `GET /api/v1/videos/popular/` - Get popular videos
- `GET /api/v1/videos/category/{category_slug}/` - Videos by category

### Surveys
- `GET /api/v1/surveys/` - List all published surveys
- `GET /api/v1/surveys/{slug}/` - Get survey details
- `GET /api/v1/surveys/latest/` - Get latest surveys
- `GET /api/v1/surveys/popular/` - Get popular surveys
- `GET /api/v1/surveys/category/{category_slug}/` - Surveys by category

## Error Handling

```typescript
async function fetchWithErrorHandling<T>(url: string): Promise<T> {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}
```

## CORS Configuration

Django backend มี CORS enabled แล้ว สามารถเรียกใช้จาก Next.js ได้โดยตรง

## Cache Strategy

```typescript
// Revalidate every hour
fetch(url, { next: { revalidate: 3600 } })

// No cache (always fresh)
fetch(url, { cache: 'no-store' })

// Cache forever
fetch(url, { cache: 'force-cache' })
```

---

**Last Updated**: November 19, 2025
**Django API Version**: v1
**Next.js Compatibility**: 13.x, 14.x, 15.x
