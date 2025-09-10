from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Category
from .serializers import (
    CategorySerializer,
    TagSerializer,
    PostListSerializer,
    PostDetailSerializer
)
from taggit.models import Tag


class CategoryListView(generics.ListAPIView):
    """
    API view to list all categories with post counts
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class PostListView(generics.ListAPIView):
    """
    API view to list published posts with pagination
    Supports search by title, content, and category
    """
    serializer_class = PostListSerializer
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag_slug = self.request.query_params.get('tag', None)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        return queryset.order_by('-created_at')


class PostDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single post by slug
    Also increments view count
    """
    queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryDetailView(generics.RetrieveAPIView):
    """
    API view to get category details and its posts
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TagListView(generics.ListAPIView):
    """
    API view to list all tags
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer


@api_view(['GET'])
def posts_by_category(request, category_slug):
    """
    API endpoint to get posts by category slug
    """
    try:
        category = Category.objects.get(slug=category_slug)
        posts = Post.objects.filter(
            category=category,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        
        return Response({
            'category': CategorySerializer(category).data,
            'posts': serializer.data
        })
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)


@api_view(['GET'])
def posts_by_tag(request, tag_slug):
    """
    API endpoint to get posts by tag slug
    """
    try:
        tag = Tag.objects.get(slug=tag_slug)
        posts = Post.objects.filter(
            tags=tag,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        
        return Response({
            'tag': TagSerializer(tag).data,
            'posts': serializer.data
        })
    except Tag.DoesNotExist:
        return Response({'error': 'Tag not found'}, status=404)


@api_view(['GET'])
def latest_posts(request):
    """
    API endpoint to get latest published posts
    """
    limit = int(request.query_params.get('limit', 10))
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags').order_by('-created_at')[:limit]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def popular_posts(request):
    """
    API endpoint to get most popular posts by view count
    """
    limit = int(request.query_params.get('limit', 10))
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags').order_by('-view_count')[:limit]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)