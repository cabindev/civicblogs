from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Avg
from .social_models import SocialPost, PostAnalyticsSummary

@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = (
        'title_with_platform', 
        'post_date', 
        'likes_count', 
        'comments_count', 
        'shares_count',
        'total_engagement_display',
        'is_active'
    )
    list_filter = ('platform', 'post_date', 'is_active', 'created_by')
    search_fields = ('title', 'content_preview')
    readonly_fields = ('created_at', 'updated_at', 'total_engagement_display')
    date_hierarchy = 'post_date'
    
    fieldsets = (
        ('ข้อมูลโพสต์', {
            'fields': ('title', 'platform', 'post_url', 'content_preview', 'post_date')
        }),
        ('สถิติ Engagement', {
            'fields': (
                ('likes_count', 'comments_count'),
                ('shares_count', 'views_count'),
                'total_engagement_display'
            )
        }),
        ('ระบบ', {
            'fields': ('created_by', 'is_active', 'notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def title_with_platform(self, obj):
        platform_colors = {
            'facebook': '#1877f2',
            'instagram': '#E4405F', 
            'twitter': '#1DA1F2',
            'tiktok': '#000000',
            'youtube': '#FF0000'
        }
        color = platform_colors.get(obj.platform, '#666666')
        platform_display = obj.get_platform_display()
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span><br>'
            '<span style="color: #666;">{}</span>',
            color, platform_display, obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
        )
    title_with_platform.short_description = 'โพสต์ / แพลตฟอร์ม'
    
    def total_engagement_display(self, obj):
        total = obj.total_engagement
        if total > 1000:
            return format_html(
                '<strong style="color: #10b981; font-size: 14px;">{:,}</strong>',
                total
            )
        return format_html(
            '<strong style="color: #666; font-size: 14px;">{}</strong>',
            total
        )
    total_engagement_display.short_description = 'รวม Engagement'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(created_by=request.user)
        return qs.select_related('created_by')
    
    def save_model(self, request, obj, form, change):
        if not change:  # ถ้าเป็นการสร้างใหม่
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PostAnalyticsSummary) 
class PostAnalyticsSummaryAdmin(admin.ModelAdmin):
    list_display = (
        'month_year_display',
        'platform',
        'total_posts',
        'total_likes',
        'total_comments', 
        'total_shares',
        'avg_engagement_display'
    )
    list_filter = ('platform', 'year', 'month')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('ช่วงเวลา', {
            'fields': ('year', 'month', 'platform')
        }),
        ('สถิติรวม', {
            'fields': (
                ('total_posts', 'avg_engagement'),
                ('total_likes', 'total_comments'),
                ('total_shares', 'total_views'),
                'best_post'
            )
        }),
        ('ระบบ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def month_year_display(self, obj):
        months = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
                  'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
        return f"{months[obj.month]} {obj.year}"
    month_year_display.short_description = 'เดือน/ปี'
    
    def avg_engagement_display(self, obj):
        return format_html(
            '<strong style="color: #f59e0b;">{:.1f}</strong>',
            obj.avg_engagement
        )
    avg_engagement_display.short_description = 'เฉลี่ย Engagement'
    
    actions = ['generate_summary']
    
    def generate_summary(self, request, queryset):
        """สร้างสรุปสถิติสำหรับเดือนที่เลือก"""
        from django.utils import timezone
        from django.db.models import Sum, Avg, Max
        
        for summary in queryset:
            # คำนวณสถิติใหม่
            posts = SocialPost.objects.filter(
                platform=summary.platform,
                post_date__year=summary.year,
                post_date__month=summary.month,
                is_active=True
            )
            
            if posts.exists():
                # คำนวณค่าต่าง ๆ
                total_posts = posts.count()
                total_likes = posts.aggregate(Sum('likes_count'))['likes_count__sum'] or 0
                total_comments = posts.aggregate(Sum('comments_count'))['comments_count__sum'] or 0
                total_shares = posts.aggregate(Sum('shares_count'))['shares_count__sum'] or 0
                total_views = posts.aggregate(Sum('views_count'))['views_count__sum'] or 0
                
                avg_engagement = posts.aggregate(
                    avg_eng=Avg(models.F('likes_count') + models.F('comments_count') + models.F('shares_count'))
                )['avg_eng'] or 0.0
                
                # หาโพสต์ที่ดีที่สุด
                best_post = posts.annotate(
                    engagement=models.F('likes_count') + models.F('comments_count') + models.F('shares_count')
                ).order_by('-engagement').first()
                
                # อัปเดตข้อมูล
                summary.total_posts = total_posts
                summary.total_likes = total_likes
                summary.total_comments = total_comments
                summary.total_shares = total_shares
                summary.total_views = total_views
                summary.avg_engagement = round(avg_engagement, 1)
                summary.best_post = best_post
                summary.save()
        
        self.message_user(request, f"อัปเดตสรุปสถิติ {queryset.count()} รายการแล้ว")
    
    generate_summary.short_description = "สร้างสรุปสถิติใหม่"