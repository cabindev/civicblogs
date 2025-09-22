from rest_framework import serializers
from .models import Post, Category, Video
from taggit.models import Tag


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']
    
    def get_post_count(self, obj):
        """Get published post count for this category"""
        return obj.posts.filter(status='published').count()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post list view (lighter data)"""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category', 
            'tags', 'featured_image_url', 'created_at', 'updated_at', 
            'view_count', 'reading_time', 'status'
        ]
    
    def get_excerpt(self, obj):
        """Get post excerpt"""
        return obj.get_excerpt()
    
    def get_reading_time(self, obj):
        """Get reading time in minutes"""
        return obj.get_reading_time()
    
    def get_featured_image_url(self, obj):
        """Get full URL for featured image"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post detail view (full data)"""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.SerializerMethodField()
    featured_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'category', 
            'tags', 'featured_image_url', 'featured_image_alt',
            'meta_description', 'meta_keywords', 'created_at', 
            'updated_at', 'view_count', 'reading_time', 'status'
        ]
    
    def get_reading_time(self, obj):
        """Get reading time in minutes"""
        return obj.get_reading_time()
    
    def get_featured_image_url(self, obj):
        """Get full URL for featured image"""
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return obj.featured_image.url
        return None

class VideoListSerializer(serializers.ModelSerializer):
    """Serializer for Video list view (lighter data)"""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'slug', 'description', 'video_url', 'author', 
            'category', 'tags', 'thumbnail_url', 'thumbnail_alt',
            'created_at', 'updated_at', 'view_count', 'status'
        ]
    
    def get_thumbnail_url(self, obj):
        """Get full URL for video thumbnail"""
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None


class VideoDetailSerializer(serializers.ModelSerializer):
    """Serializer for Video detail view (full data)"""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'slug', 'description', 'video_url', 'author', 
            'category', 'tags', 'thumbnail_url', 'thumbnail_alt',
            'created_at', 'updated_at', 'view_count', 'status'
        ]
    
    def get_thumbnail_url(self, obj):
        """Get full URL for video thumbnail"""
        if obj.thumbnail:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None
