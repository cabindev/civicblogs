from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from PIL import Image
import uuid
import os
import re

# Import Social Media models (with error handling)
try:
    from .social_models import SocialPost, PostAnalyticsSummary
except ImportError:
    SocialPost = None
    PostAnalyticsSummary = None
from django.utils.html import strip_tags

# Get Azure Storage instance
# def get_azure_storage():
#     from django.conf import settings
#     from django.core.files.storage import get_storage_class
#     return get_storage_class(settings.DEFAULT_FILE_STORAGE)()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class PostType(models.Model):
    """Model to define different types of posts like infographic, news, website, etc."""
    name = models.CharField(max_length=50, unique=True, verbose_name="ชื่อประเภท")
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="คำอธิบาย")
    icon = models.CharField(max_length=20, blank=True, help_text="CSS icon class or emoji", verbose_name="ไอคอน")
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code", verbose_name="สีประจำประเภท")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'ประเภทโพสต์'
        verbose_name_plural = 'ประเภทโพสต์'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def upload_featured_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('blog/featured_images', filename)


def upload_video_thumbnail(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('blog/video_thumbnails', filename)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    post_type = models.ForeignKey(PostType, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="ประเภทโพสต์")
    content = RichTextUploadingField(help_text='เนื้อหาบทความ - รองรับการอัปโหลดรูปภาพ')
    featured_image = models.ImageField(upload_to=upload_featured_image, blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True, help_text='Alt text for featured image')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager(blank=True)
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # For Thai text, create a simple slug from title
            import re
            from django.utils import timezone
            
            slug_text = self.title.lower()
            # Remove Thai characters and keep only English and numbers
            slug_text = re.sub(r'[^\w\s-]', '', slug_text)
            slug_text = re.sub(r'[-\s]+', '-', slug_text)
            
            # If no English characters, use a generic slug with timestamp
            if not slug_text or slug_text == '-':
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                slug_text = f"post-{timestamp}"
            
            # Ensure slug is not empty and is valid
            base_slug = slugify(slug_text) or f"post-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            # Check for uniqueness and add number if needed
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
        
        # Optimize image for both local and cloud storage
        if self.featured_image:
            try:
                from django.core.files.storage import default_storage
                from django.core.files.base import ContentFile
                from io import BytesIO
                
                # Open image from uploaded file
                if hasattr(self.featured_image, 'file'):
                    img = Image.open(self.featured_image.file)
                else:
                    img = Image.open(self.featured_image)
                
                # Convert RGBA to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize image if it's larger than 1200x800
                max_width, max_height = 1200, 800
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Save optimized image to BytesIO
                output = BytesIO()
                img.save(output, format='JPEG', optimize=True, quality=85)
                output.seek(0)
                
                # For cloud storage, replace the file content
                if 'FileSystemStorage' not in str(default_storage.__class__):
                    # Get original filename
                    original_name = self.featured_image.name
                    if not original_name:
                        import uuid
                        original_name = f'{uuid.uuid4()}.jpg'
                    elif not original_name.lower().endswith('.jpg'):
                        original_name = original_name.rsplit('.', 1)[0] + '.jpg'
                    
                    # Create new file with optimized content
                    optimized_file = ContentFile(output.getvalue(), name=original_name)
                    self.featured_image = optimized_file
                else:
                    # For local storage, save directly to path after model save
                    pass
                    
                print(f"✅ Image optimized: {img.width}x{img.height}")
                
            except Exception as e:
                # Don't fail the save if image optimization fails
                print(f"⚠️ Image optimization skipped due to error: {e}")
                pass
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_reading_time(self):
        # Strip HTML tags for word count
        plain_text = strip_tags(self.content)
        word_count = len(plain_text.split())
        return max(1, round(word_count / 200))
    
    def get_excerpt(self):
        """Generate excerpt automatically from content"""
        # Remove HTML tags
        plain_text = strip_tags(self.content)
        
        # Clean up text
        plain_text = re.sub(r'\s+', ' ', plain_text).strip()
        
        # Get first 150 characters for excerpt
        if len(plain_text) > 150:
            # Try to break at sentence end
            excerpt = plain_text[:150]
            last_sentence = excerpt.rfind('.')
            last_space = excerpt.rfind(' ')
            
            if last_sentence > 100:
                return excerpt[:last_sentence + 1]
            elif last_space > 100:
                return excerpt[:last_space] + '...'
            else:
                return excerpt + '...'
        
        return plain_text


class Video(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    
    title = models.CharField(max_length=200, help_text='ชื่อวิดีโอ')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, help_text='คำอธิบายวิดีโอ')
    video_url = models.URLField(help_text='ลิงก์วิดีโอ เช่น https://www.facebook.com/reel/791446180047418')
    thumbnail = models.ImageField(upload_to=upload_video_thumbnail, blank=True, null=True, help_text='รูปปกวิดีโอ')
    thumbnail_alt = models.CharField(max_length=200, blank=True, help_text='Alt text สำหรับรูปปก')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # For Thai text, create a simple slug from title
            import re
            from django.utils import timezone
            
            slug_text = self.title.lower()
            # Remove Thai characters and keep only English and numbers
            slug_text = re.sub(r'[^\w\s-]', '', slug_text)
            slug_text = re.sub(r'[-\s]+', '-', slug_text)
            
            # If no English characters, use a generic slug with timestamp
            if not slug_text or slug_text == '-':
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                slug_text = f"video-{timestamp}"
            
            # Make sure slug is unique
            base_slug = slugify(slug_text) or f"video-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            slug = base_slug
            counter = 1
            
            # Check if slug exists and make it unique
            while Video.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:video_detail', kwargs={'slug': self.slug})


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.subject} - {self.name}'
