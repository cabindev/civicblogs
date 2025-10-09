from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Category, PostType, Video, Survey
from .serializers import (
    CategorySerializer,
    PostTypeSerializer,
    TagSerializer,
    PostListSerializer,
    PostDetailSerializer,
    VideoListSerializer,
    VideoDetailSerializer,
    SurveyListSerializer,
    SurveyDetailSerializer
)
from taggit.models import Tag


class CategoryListView(generics.ListAPIView):
    """
    API view to list all categories with post counts
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class PostTypeListView(generics.ListAPIView):
    """
    API view to list all post types with post counts
    """
    queryset = PostType.objects.all().order_by('name')
    serializer_class = PostTypeSerializer


class PostListView(generics.ListAPIView):
    """
    API view to list published posts with pagination
    Supports search by title, content, and category
    """
    serializer_class = PostListSerializer
    pagination_class = None  # Disable pagination temporarily for Next.js compatibility
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category', 'post_type').prefetch_related('tags')
        
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
    queryset = Post.objects.filter(status='published').select_related('author', 'category', 'post_type').prefetch_related('tags')
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
        ).select_related('author', 'category', 'post_type').prefetch_related('tags').order_by('-created_at')
        
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
        ).select_related('author', 'category', 'post_type').prefetch_related('tags').order_by('-created_at')
        
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
    posts = Post.objects.filter(status='published').select_related('author', 'category', 'post_type').prefetch_related('tags').order_by('-created_at')[:limit]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def popular_posts(request):
    """
    API endpoint to get most popular posts by view count
    """
    limit = int(request.query_params.get('limit', 10))
    posts = Post.objects.filter(status='published').select_related('author', 'category', 'post_type').prefetch_related('tags').order_by('-view_count')[:limit]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

class VideoListView(generics.ListAPIView):
    """
    API view to list published videos with pagination
    Supports search by title, description, and category
    """
    serializer_class = VideoListSerializer
    
    def get_queryset(self):
        queryset = Video.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
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


class VideoDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single video by slug
    Also increments view count
    """
    queryset = Video.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    serializer_class = VideoDetailSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['GET'])
def latest_videos(request):
    """
    API endpoint to get latest published videos
    """
    limit = int(request.query_params.get('limit', 10))
    if limit > 50:  # Maximum limit
        limit = 50
    
    videos = Video.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags').order_by('-created_at')[:limit]
    
    serializer = VideoListSerializer(videos, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def popular_videos(request):
    """
    API endpoint to get most popular videos by view count
    """
    limit = int(request.query_params.get('limit', 10))
    if limit > 50:  # Maximum limit
        limit = 50
        
    videos = Video.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags').order_by('-view_count')[:limit]
    
    serializer = VideoListSerializer(videos, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def videos_by_category(request, category_slug):
    """
    API endpoint to get videos by category slug
    """
    try:
        category = Category.objects.get(slug=category_slug)
        videos = Video.objects.filter(
            category=category,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')
        
        serializer = VideoListSerializer(videos, many=True, context={'request': request})
        
        return Response({
            'category': CategorySerializer(category).data,
            'videos': serializer.data
        })
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)


@api_view(['GET'])
def videos_by_tag(request, tag_slug):
    """
    API endpoint to get videos by tag slug
    """
    try:
        tag = Tag.objects.get(slug=tag_slug)
        videos = Video.objects.filter(
            tags=tag,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')

        serializer = VideoListSerializer(videos, many=True, context={'request': request})

        return Response({
            'tag': TagSerializer(tag).data,
            'videos': serializer.data
        })
    except Tag.DoesNotExist:
        return Response({'error': 'Tag not found'}, status=404)


# Survey API Views
class SurveyListView(generics.ListAPIView):
    """
    API view to list published surveys with pagination
    Supports search by title and description
    """
    serializer_class = SurveyListSerializer

    def get_queryset(self):
        queryset = Survey.objects.filter(is_published=True).select_related('author', 'category')

        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )

        # Filter by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.order_by('-created_at')


class SurveyDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single survey by slug
    Also increments view count
    """
    queryset = Survey.objects.filter(is_published=True).select_related('author', 'category')
    serializer_class = SurveyDetailSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.view_count += 1
        instance.save(update_fields=['view_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['GET'])
def latest_surveys(request):
    """
    API endpoint to get latest published surveys
    """
    limit = int(request.query_params.get('limit', 10))
    if limit > 50:  # Maximum limit
        limit = 50

    surveys = Survey.objects.filter(is_published=True).select_related('author', 'category').order_by('-created_at')[:limit]

    serializer = SurveyListSerializer(surveys, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def popular_surveys(request):
    """
    API endpoint to get most popular surveys by view count
    """
    limit = int(request.query_params.get('limit', 10))
    if limit > 50:  # Maximum limit
        limit = 50

    surveys = Survey.objects.filter(is_published=True).select_related('author', 'category').order_by('-view_count')[:limit]

    serializer = SurveyListSerializer(surveys, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def surveys_by_category(request, category_slug):
    """
    API endpoint to get surveys by category slug
    """
    try:
        category = Category.objects.get(slug=category_slug)
        surveys = Survey.objects.filter(
            category=category,
            is_published=True
        ).select_related('author', 'category').order_by('-created_at')

        serializer = SurveyListSerializer(surveys, many=True, context={'request': request})

        return Response({
            'category': CategorySerializer(category).data,
            'surveys': serializer.data
        })
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=404)
