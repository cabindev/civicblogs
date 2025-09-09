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


def upload_featured_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('blog/featured_images', filename)


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
            slug_text = self.title.lower()
            # Remove Thai characters and keep only English and numbers
            slug_text = re.sub(r'[^\w\s-]', '', slug_text)
            slug_text = re.sub(r'[-\s]+', '-', slug_text)
            
            # If no English characters, use a generic slug with ID
            if not slug_text or slug_text == '-':
                slug_text = f"post-{self.id or 'new'}-{self.title[:20]}"
            
            # Ensure slug is not empty and is valid
            self.slug = slugify(slug_text) or f"post-{self.id or 'new'}"
        
        super().save(*args, **kwargs)
        
        # Only optimize image if using local file storage (not cloud storage)
        if self.featured_image:
            try:
                from django.core.files.storage import default_storage
                # Check if we're using local file storage (FileSystemStorage)
                if 'FileSystemStorage' in str(default_storage.__class__):
                    img = Image.open(self.featured_image.path)
                    
                    # Resize image if it's larger than 1200x800
                    if img.height > 800 or img.width > 1200:
                        img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
                        img.save(self.featured_image.path, optimize=True, quality=85)
                else:
                    # Skip image optimization for cloud storage (Azure, S3, etc.)
                    print(f"Skipping image optimization for {default_storage.__class__.__name__}")
            except Exception as e:
                # Don't fail the save if image optimization fails
                print(f"Image optimization skipped due to error: {e}")
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
