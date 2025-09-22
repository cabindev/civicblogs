from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    # Categories
    path('categories/', api_views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', api_views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<slug:category_slug>/posts/', api_views.posts_by_category, name='posts-by-category'),
    
    # Tags
    path('tags/', api_views.TagListView.as_view(), name='tag-list'),
    path('tags/<slug:tag_slug>/posts/', api_views.posts_by_tag, name='posts-by-tag'),
    
    # Posts
    path('posts/', api_views.PostListView.as_view(), name='post-list'),
    path('posts/latest/', api_views.latest_posts, name='latest-posts'),
    path('posts/popular/', api_views.popular_posts, name='popular-posts'),
    path('posts/<slug:slug>/', api_views.PostDetailView.as_view(), name='post-detail'),
    
    # Videos
    path('videos/', api_views.VideoListView.as_view(), name='video-list'),
    path('videos/latest/', api_views.latest_videos, name='latest-videos'),
    path('videos/popular/', api_views.popular_videos, name='popular-videos'),
    path('videos/<slug:slug>/', api_views.VideoDetailView.as_view(), name='video-detail'),
    
    # Videos by category and tag
    path('categories/<slug:category_slug>/videos/', api_views.videos_by_category, name='videos-by-category'),
    path('tags/<slug:tag_slug>/videos/', api_views.videos_by_tag, name='videos-by-tag'),
]