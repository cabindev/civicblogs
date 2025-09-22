from django.urls import path, re_path
from . import views
try:
    from . import social_views
except ImportError:
    social_views = None

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    re_path(r'^video/(?P<slug>[-\w]+)/$', views.VideoDetailView.as_view(), name='video_detail'),
    re_path(r'^category/(?P<slug>[-\w]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    re_path(r'^tag/(?P<slug>.+)/$', views.TaggedPostsView.as_view(), name='tagged_posts'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Social Media Analytics URLs (conditional)
] + ([] if social_views is None else [
    path('social/', social_views.social_dashboard, name='social_dashboard'),
    path('social/posts/', social_views.social_posts_table, name='social_posts_table'),
    path('social/reports/', social_views.social_monthly_report, name='social_monthly_report'),
]) + [
]