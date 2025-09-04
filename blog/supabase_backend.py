"""
Supabase Backend Integration for CivicBlogs
Uses Supabase REST API instead of direct PostgreSQL connection
"""

from supabase import create_client, Client
from django.conf import settings
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

class SupabaseBackend:
    """Handle Supabase operations via REST API"""
    
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
    
    # Category Operations
    def create_category(self, data: Dict) -> Dict:
        """Create a new category in Supabase"""
        try:
            result = self.supabase.table('categories').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating category: {e}")
            return None
    
    def get_categories(self, active_only: bool = True) -> List[Dict]:
        """Get all categories"""
        try:
            query = self.supabase.table('categories').select('*')
            if active_only:
                query = query.eq('is_active', True)
            result = query.order('sort_order', desc=False).execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def update_category(self, category_id: str, data: Dict) -> Dict:
        """Update a category"""
        try:
            result = self.supabase.table('categories').update(data).eq('id', category_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating category: {e}")
            return None
    
    # Post Operations
    def create_post(self, data: Dict) -> Dict:
        """Create a new post in Supabase"""
        try:
            # Ensure required fields
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
            if 'created_at' not in data:
                data['created_at'] = datetime.now().isoformat()
            
            result = self.supabase.table('posts').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating post: {e}")
            return None
    
    def get_posts(self, status: str = 'published', limit: int = 10) -> List[Dict]:
        """Get posts from Supabase"""
        try:
            result = self.supabase.table('posts')\
                .select('*, categories(name, slug), profiles(username)')\
                .eq('status', status)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting posts: {e}")
            return []
    
    def get_post_by_slug(self, slug: str) -> Optional[Dict]:
        """Get a single post by slug"""
        try:
            result = self.supabase.table('posts')\
                .select('*, categories(name, slug), profiles(username)')\
                .eq('slug', slug)\
                .eq('status', 'published')\
                .single()\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error getting post by slug: {e}")
            return None
    
    def update_post(self, post_id: str, data: Dict) -> Dict:
        """Update a post"""
        try:
            data['updated_at'] = datetime.now().isoformat()
            result = self.supabase.table('posts').update(data).eq('id', post_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating post: {e}")
            return None
    
    def increment_post_views(self, post_id: str) -> bool:
        """Increment post view count"""
        try:
            # First get current count
            post = self.supabase.table('posts').select('view_count').eq('id', post_id).single().execute()
            if post.data:
                new_count = (post.data.get('view_count', 0) or 0) + 1
                self.supabase.table('posts').update({'view_count': new_count}).eq('id', post_id).execute()
                return True
            return False
        except Exception as e:
            print(f"Error incrementing views: {e}")
            return False
    
    # Tag Operations
    def create_tag(self, data: Dict) -> Dict:
        """Create a new tag"""
        try:
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
            result = self.supabase.table('tags').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating tag: {e}")
            return None
    
    def get_tags(self, limit: int = 50) -> List[Dict]:
        """Get all tags"""
        try:
            result = self.supabase.table('tags')\
                .select('*')\
                .order('usage_count', desc=True)\
                .limit(limit)\
                .execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting tags: {e}")
            return []
    
    def get_posts_by_tag(self, tag_slug: str, limit: int = 10) -> List[Dict]:
        """Get posts by tag"""
        try:
            # First get tag ID
            tag_result = self.supabase.table('tags').select('id').eq('slug', tag_slug).single().execute()
            if not tag_result.data:
                return []
            
            tag_id = tag_result.data['id']
            
            # Get post IDs from post_tags
            post_tags = self.supabase.table('post_tags')\
                .select('post_id')\
                .eq('tag_id', tag_id)\
                .execute()
            
            if not post_tags.data:
                return []
            
            post_ids = [pt['post_id'] for pt in post_tags.data]
            
            # Get posts
            result = self.supabase.table('posts')\
                .select('*, categories(name, slug), profiles(username)')\
                .in_('id', post_ids)\
                .eq('status', 'published')\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data or []
        except Exception as e:
            print(f"Error getting posts by tag: {e}")
            return []
    
    # Comment Operations
    def create_comment(self, data: Dict) -> Dict:
        """Create a comment"""
        try:
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
            result = self.supabase.table('comments').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating comment: {e}")
            return None
    
    def get_comments_for_post(self, post_id: str) -> List[Dict]:
        """Get approved comments for a post"""
        try:
            result = self.supabase.table('comments')\
                .select('*')\
                .eq('post_id', post_id)\
                .eq('is_approved', True)\
                .eq('is_spam', False)\
                .order('created_at', desc=False)\
                .execute()
            return result.data or []
        except Exception as e:
            print(f"Error getting comments: {e}")
            return []
    
    # Newsletter Operations
    def subscribe_newsletter(self, email: str) -> bool:
        """Subscribe to newsletter"""
        try:
            data = {
                'id': str(uuid.uuid4()),
                'email': email,
                'status': 'active',
                'subscribed_at': datetime.now().isoformat()
            }
            result = self.supabase.table('newsletter_subscribers').upsert(data).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error subscribing to newsletter: {e}")
            return False
    
    # Contact Operations
    def create_contact_message(self, data: Dict) -> bool:
        """Create a contact message"""
        try:
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
            if 'created_at' not in data:
                data['created_at'] = datetime.now().isoformat()
            
            result = self.supabase.table('contact_messages').insert(data).execute()
            return bool(result.data)
        except Exception as e:
            print(f"Error creating contact message: {e}")
            return False
    
    # Search Operations
    def search_posts(self, query: str, limit: int = 10) -> List[Dict]:
        """Search posts by title and content"""
        try:
            # Supabase full-text search using ilike
            result = self.supabase.table('posts')\
                .select('*, categories(name, slug), profiles(username)')\
                .or_(f"title.ilike.%{query}%,content.ilike.%{query}%,excerpt.ilike.%{query}%")\
                .eq('status', 'published')\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return result.data or []
        except Exception as e:
            print(f"Error searching posts: {e}")
            return []

# Global instance
supabase_backend = SupabaseBackend()