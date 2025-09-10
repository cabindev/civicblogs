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
]