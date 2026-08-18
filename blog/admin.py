from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Post, Category, PostType, Newsletter, ContactMessage, Video, Survey

# Customize admin site
admin.site.site_header = "การจัดการ Civicspace"
admin.site.site_title = "Civicspace Admin"
admin.site.index_title = "ยินดีต้อนรับสู่ระบบจัดการ Civicspace"



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'video_count', 'survey_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'

    def survey_count(self, obj):
        return obj.surveys.count()
    survey_count.short_description = 'Surveys'


@admin.register(PostType)
class PostTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'icon', 'color', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


class RequireCategoryForm(forms.ModelForm):
    """บังคับเลือกประเด็นก่อนบันทึก

    หน้าเว็บ Next.js อ่าน category.name ตรง ๆ หลายจุดโดยไม่กัน null
    โพสต์ที่เผยแพร่โดยไม่มีประเด็นจึงทำให้หน้าแรกพังทั้งหน้า
    ถ้าเนื้อหาไม่เข้ากับประเด็นที่ทำอยู่ ให้เลือก "อื่นๆ"
    """

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.fields:
            self.fields['category'].required = True
            self.fields['category'].empty_label = '— เลือกประเด็น —'
            self.fields['category'].help_text = (
                'ต้องเลือกเสมอ ถ้าไม่เข้ากับประเด็นที่ทำอยู่ให้เลือก "อื่นๆ"'
            )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = RequireCategoryForm
    list_display = ['get_featured_image_thumbnail', 'title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'category']
    search_fields = ['title', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
    actions = ['mark_as_published', 'mark_as_draft']
    
    fields = ('title', 'slug', 'author', 'category', 'post_type', 'content', 'featured_image', 'featured_image_alt', 'status', 'tags', 'meta_description', 'published_at')
    
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
    
    def get_featured_image_thumbnail(self, obj):
        """Display small thumbnail of featured image in admin list"""
        if obj.featured_image:
            try:
                return format_html(
                    '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e5e7eb;" />',
                    obj.featured_image.url
                )
            except Exception as e:
                return format_html(
                    '<div style="width: 40px; height: 40px; background: linear-gradient(135deg, #fee2e2, #fecaca); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #dc2626; text-align: center; border: 1px solid #f87171;">❌<br>Error</div>'
                )
        return format_html(
            '<div style="width: 40px; height: 40px; background: linear-gradient(135deg, #f3f4f6, #e5e7eb); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #6b7280; text-align: center; border: 1px solid #d1d5db;">📷<br>No</div>'
        )
    get_featured_image_thumbnail.short_description = '🖼️'
    get_featured_image_thumbnail.allow_tags = True


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = RequireCategoryForm
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


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'respondent_count', 'view_count', 'survey_date', 'created_at']
    list_filter = ['is_published', 'created_at', 'survey_date', 'category']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['mark_as_published', 'mark_as_unpublished']

    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('title', 'slug', 'description', 'author', 'category')
        }),
        ('ไฟล์แบบสำรวจ', {
            'fields': ('survey_file',),
            'description': 'อัปโหลดไฟล์แบบสำรวจ (Word/Excel)'
        }),
        ('การเผยแพร่', {
            'fields': ('is_published', 'published_at'),
            'description': 'เผยแพร่เอกสารการสำรวจให้สาธารณะเห็น'
        }),
        ('วันที่สำรวจ', {
            'fields': ('survey_date',),
            'description': 'วันที่ทำการสำรวจ'
        }),
        ('สถิติ', {
            'fields': ('respondent_count', 'view_count'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['respondent_count', 'view_count', 'published_at']

    def mark_as_published(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for survey in queryset:
            survey.is_published = True
            if not survey.published_at:
                survey.published_at = timezone.now()
            survey.save()
            updated += 1
        self.message_user(request, f'{updated} แบบสำรวจถูกเผยแพร่แล้ว')
    mark_as_published.short_description = "เผยแพร่"

    def mark_as_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f'{queryset.count()} แบบสำรวจถูกยกเลิกการเผยแพร่แล้ว')
    mark_as_unpublished.short_description = "ยกเลิกการเผยแพร่"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
