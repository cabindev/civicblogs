from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Post, Category, Newsletter, ContactMessage, Video

# Import Social Media Admin (with error handling)
try:
    from .social_admin import SocialPostAdmin, PostAnalyticsSummaryAdmin
except ImportError:
    SocialPostAdmin = None
    PostAnalyticsSummaryAdmin = None


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'created_at', 'published_at']
    list_filter = ['status', 'created_at', 'category', 'tags']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['mark_as_published', 'mark_as_draft', 'delete_selected_posts']
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('เนื้อหา', {
            'fields': ('content',)
        }),
        ('รูปภาพ', {
            'fields': ('featured_image', 'featured_image_alt')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('แท็ก', {
            'fields': ('tags',)
        }),
        ('การเผยแพร่', {
            'fields': ('published_at',)
        }),
    )
    
    def mark_as_published(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for post in queryset:
            post.status = 'published'
            if not post.published_at:
                post.published_at = timezone.now()
            post.save()
            updated += 1
        self.message_user(request, f'{updated} บทความได้รับการเผยแพร่แล้ว')
    mark_as_published.short_description = "เผยแพร่บทความที่เลือก"
    
    def mark_as_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f'{queryset.count()} บทความถูกเปลี่ยนเป็น Draft แล้ว')
    mark_as_draft.short_description = "เปลี่ยนเป็น Draft"
    
    def delete_selected_posts(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} บทความถูกลบแล้ว')
    delete_selected_posts.short_description = "ลบบทความที่เลือก"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'created_at', 'published_at']
    list_filter = ['status', 'created_at', 'category', 'tags']
    search_fields = ['title', 'description', 'author__username', 'video_url']
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['mark_as_published', 'mark_as_draft']
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('title', 'slug', 'author', 'category', 'status'),
            'description': 'Slug สามารถเว้นว่างได้ (ระบบจะสร้างให้อัตโนมัติ)'
        }),
        ('วิดีโอ', {
            'fields': ('video_url', 'description')
        }),
        ('รูปภาพ', {
            'fields': ('thumbnail', 'thumbnail_alt')
        }),
        ('แท็ก', {
            'fields': ('tags',)
        }),
        ('การเผยแพร่', {
            'fields': ('published_at',)
        }),
    )
    
    def mark_as_published(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for video in queryset:
            video.status = 'published'
            if not video.published_at:
                video.published_at = timezone.now()
            video.save()
            updated += 1
        self.message_user(request, f'{updated} วิดีโอได้รับการเผยแพร่แล้ว')
    mark_as_published.short_description = "เผยแพร่วิดีโอที่เลือก"
    
    def mark_as_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f'{queryset.count()} วิดีโอถูกเปลี่ยนเป็น Draft แล้ว')
    mark_as_draft.short_description = "เปลี่ยนเป็น Draft"
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} subscriptions activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} subscriptions deactivated.')
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} messages marked as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"
