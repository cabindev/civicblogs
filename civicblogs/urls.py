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
    <html lang="th">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>CivicSpace - แพลตฟอร์มสื่อสารสาธารณะ</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Kanit', sans-serif; }
        </style>
    </head>
    <body class="bg-gradient-to-br from-yellow-50 via-white to-yellow-100 min-h-screen">
        <!-- Hero Section -->
        <div class="container mx-auto px-4 py-16">
            <div class="text-center mb-16">
                <div class="inline-flex items-center gap-3 mb-6">
                    <div class="w-16 h-16 bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center">
                        <span class="text-2xl">🎥</span>
                    </div>
                    <h1 class="text-5xl font-bold bg-gradient-to-r from-yellow-600 to-yellow-800 bg-clip-text text-transparent">
                        CivicSpace
                    </h1>
                </div>
                <p class="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
                    แพลตฟอร์มสื่อสารสาธารณะ สำหรับแบ่งปันเรื่องราวและวิดีโอ เพื่อสร้างการมีส่วนร่วมในสังคม
                </p>
            </div>

            <!-- API Statistics -->
            <div class="grid md:grid-cols-3 gap-8 mb-16">
                <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100">
                    <div class="text-3xl mb-4">📹</div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2">Video API</h3>
                    <p class="text-gray-600">ระบบจัดการวิดีโอครบครัน พร้อม analytics และ search</p>
                </div>
                <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100">
                    <div class="text-3xl mb-4">📝</div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2">Blog System</h3>
                    <p class="text-gray-600">ระบบบล็อกพร้อม CKEditor และระบบ tagging</p>
                </div>
                <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100">
                    <div class="text-3xl mb-4">🔗</div>
                    <h3 class="text-2xl font-semibold text-gray-800 mb-2">REST API</h3>
                    <p class="text-gray-600">API สำหรับ Next.js พร้อม CORS และ pagination</p>
                </div>
            </div>

            <!-- API Endpoints -->
            <div class="bg-white rounded-2xl p-8 shadow-lg border border-yellow-100 mb-12">
                <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">🚀 API Endpoints</h2>
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <h3 class="text-xl font-semibold text-yellow-700 border-b border-yellow-200 pb-2">📹 Video API</h3>
                        <div class="space-y-2">
                            <a href="/api/v1/videos/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/videos/</code>
                                <span class="text-gray-600 ml-2">รายการวิดีโอทั้งหมด</span>
                            </a>
                            <a href="/api/v1/videos/latest/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/videos/latest/</code>
                                <span class="text-gray-600 ml-2">วิดีโอล่าสุด</span>
                            </a>
                            <a href="/api/v1/videos/popular/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/videos/popular/</code>
                                <span class="text-gray-600 ml-2">วิดีโอยอดนิยม</span>
                            </a>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <h3 class="text-xl font-semibold text-yellow-700 border-b border-yellow-200 pb-2">📝 Content API</h3>
                        <div class="space-y-2">
                            <a href="/api/v1/posts/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/posts/</code>
                                <span class="text-gray-600 ml-2">รายการบทความ</span>
                            </a>
                            <a href="/api/v1/categories/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/categories/</code>
                                <span class="text-gray-600 ml-2">หมวดหมู่</span>
                            </a>
                            <a href="/api/v1/tags/" class="block p-3 rounded-lg bg-yellow-50 hover:bg-yellow-100 transition-colors">
                                <code class="text-yellow-700">/api/v1/tags/</code>
                                <span class="text-gray-600 ml-2">แท็ก</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Features -->
            <div class="bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-2xl p-8 text-white mb-12">
                <h2 class="text-3xl font-bold mb-8 text-center">✨ คุณสมบัติเด่น</h2>
                <div class="grid md:grid-cols-2 gap-8">
                    <div class="space-y-4">
                        <div class="flex items-start gap-3">
                            <span class="text-xl">🔍</span>
                            <div>
                                <h4 class="font-semibold">ระบบค้นหาข้อมูล</h4>
                                <p class="text-yellow-100">ค้นหาในเนื้อหา ชื่อเรื่อง และหมวดหมู่</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-xl">📊</span>
                            <div>
                                <h4 class="font-semibold">Analytics & Metrics</h4>
                                <p class="text-yellow-100">ติดตามยอดเข้าชมและสถิติการใช้งาน</p>
                            </div>
                        </div>
                    </div>
                    <div class="space-y-4">
                        <div class="flex items-start gap-3">
                            <span class="text-xl">📱</span>
                            <div>
                                <h4 class="font-semibold">Responsive Design</h4>
                                <p class="text-yellow-100">รองรับทุกขนาดหน้าจอ Mobile-first</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <span class="text-xl">☁️</span>
                            <div>
                                <h4 class="font-semibold">Azure Cloud Storage</h4>
                                <p class="text-yellow-100">จัดเก็บไฟล์มีเดียบน Azure Blob Storage</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Admin & Documentation -->
            <div class="grid md:grid-cols-2 gap-8">
                <div class="text-center">
                    <a href="/admin/" class="inline-flex items-center gap-3 bg-gray-800 text-white px-8 py-4 rounded-xl hover:bg-gray-700 transition-colors text-lg font-medium">
                        <span>⚙️</span>
                        Admin Panel
                    </a>
                </div>
                <div class="text-center">
                    <a href="/debug/" class="inline-flex items-center gap-3 bg-blue-600 text-white px-8 py-4 rounded-xl hover:bg-blue-700 transition-colors text-lg font-medium">
                        <span>🔧</span>
                        Debug Info
                    </a>
                </div>
            </div>

            <!-- Footer -->
            <div class="text-center mt-16 text-gray-500">
                <p>Built with Django 5.2.5 • PostgreSQL • Azure Cloud • Next.js Ready</p>
                <p class="mt-2">🤖 Generated with <a href="https://claude.ai/code" class="text-yellow-600 hover:underline">Claude Code</a></p>
            </div>
        </div>
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
