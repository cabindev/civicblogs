from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SocialPost(models.Model):
    """โพสต์บนโซเชียลมีเดีย (Facebook, Instagram, etc.)"""
    
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'), 
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ]
    
    title = models.CharField('หัวข้อโพสต์', max_length=200)
    platform = models.CharField('แพลตฟอร์ม', max_length=20, choices=PLATFORM_CHOICES, default='facebook')
    post_url = models.URLField('ลิงก์โพสต์', blank=True, null=True)
    content_preview = models.TextField('เนื้อหาโพสต์', blank=True, help_text='เนื้อหาโพสต์ (ย่อ)')
    
    # Engagement metrics
    likes_count = models.PositiveIntegerField('จำนวน Like', default=0)
    comments_count = models.PositiveIntegerField('จำนวน Comment', default=0)  
    shares_count = models.PositiveIntegerField('จำนวน Share', default=0)
    views_count = models.PositiveIntegerField('จำนวน View', default=0, help_text='สำหรับ Video posts')
    
    # Metadata
    post_date = models.DateTimeField('วันที่โพสต์', default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='สร้างโดย')
    created_at = models.DateTimeField('สร้างเมื่อ', auto_now_add=True)
    updated_at = models.DateTimeField('อัปเดตเมื่อ', auto_now=True)
    
    # Status
    is_active = models.BooleanField('เปิดใช้งาน', default=True)
    notes = models.TextField('หมายเหตุ', blank=True)
    
    class Meta:
        verbose_name = 'โพสต์โซเชียล'
        verbose_name_plural = 'โพสต์โซเชียล'
        ordering = ['-post_date']
    
    def __str__(self):
        return f"{self.get_platform_display()}: {self.title}"
    
    @property
    def total_engagement(self):
        """รวม engagement ทั้งหมด"""
        return self.likes_count + self.comments_count + self.shares_count
    
    @property
    def engagement_rate(self):
        """คำนวณ engagement rate (ถ้ามี views)"""
        if self.views_count > 0:
            return round((self.total_engagement / self.views_count) * 100, 2)
        return 0


class PostAnalyticsSummary(models.Model):
    """สรุปสถิติโพสต์รายเดือน"""
    
    year = models.PositiveIntegerField('ปี')
    month = models.PositiveIntegerField('เดือน', choices=[(i, i) for i in range(1, 13)])
    platform = models.CharField('แพลตฟอร์ม', max_length=20, choices=SocialPost.PLATFORM_CHOICES)
    
    # Summary metrics
    total_posts = models.PositiveIntegerField('จำนวนโพสต์', default=0)
    total_likes = models.PositiveIntegerField('รวม Like', default=0)
    total_comments = models.PositiveIntegerField('รวม Comment', default=0)
    total_shares = models.PositiveIntegerField('รวม Share', default=0)
    total_views = models.PositiveIntegerField('รวม View', default=0)
    
    avg_engagement = models.FloatField('เฉลี่ย Engagement', default=0.0)
    best_post = models.ForeignKey(SocialPost, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='โพสต์ที่ดีที่สุด')
    
    created_at = models.DateTimeField('สร้างเมื่อ', auto_now_add=True)
    updated_at = models.DateTimeField('อัปเดตเมื่อ', auto_now=True)
    
    class Meta:
        verbose_name = 'สรุปสถิติโพสต์'
        verbose_name_plural = 'สรุปสถิติโพสต์' 
        unique_together = ['year', 'month', 'platform']
        ordering = ['-year', '-month', 'platform']
    
    def __str__(self):
        months = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
                  'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
        return f"{months[self.month]} {self.year} - {self.get_platform_display()}"