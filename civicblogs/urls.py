"""
URL configuration for civicblogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse

# Simple test view for debugging
def test_view(request):
    return HttpResponse("<h1>Django is working!</h1><p>Test view successfully loaded</p>")

def debug_info(request):
    import sys
    import django
    info = f"""
    <h1>Debug Info</h1>
    <p>Django Version: {django.VERSION}</p>
    <p>Python Version: {sys.version}</p>
    <p>DEBUG: {settings.DEBUG}</p>
    <p>Database: {settings.DATABASES['default']['ENGINE']}</p>
    """
    return HttpResponse(info)

def simple_homepage(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CivicSpace</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>🎥 CivicSpace - Video API Ready</h1>
        <p>Homepage temporarily simplified for debugging</p>
        <h2>Available API Endpoints:</h2>
        <ul>
            <li><a href="/api/v1/videos/">/api/v1/videos/</a></li>
            <li><a href="/api/v1/videos/latest/">/api/v1/videos/latest/</a></li>
            <li><a href="/api/v1/videos/popular/">/api/v1/videos/popular/</a></li>
            <li><a href="/api/v1/posts/">/api/v1/posts/</a></li>
            <li><a href="/api/v1/categories/">/api/v1/categories/</a></li>
        </ul>
        <p><a href="/admin/">Admin Panel</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('blog.api_urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    # Debug URLs
    path('test/', test_view, name='test'),
    path('debug/', debug_info, name='debug'),
    # Temporary simple homepage to bypass blog view errors
    path('', simple_homepage, name='homepage'),
    # Commented out problematic blog URLs for now
    # path('', include('blog.urls')),
]

# Serve media files in both development and production
# Note: For production, consider using Azure Blob Storage for better performance
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
