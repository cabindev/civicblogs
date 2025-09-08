#!/usr/bin/env python3
"""
Migrate existing local images to Azure Blob Storage
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'civicblogs.settings')
sys.path.append('/Applications/MAMP/htdocs/civicblogs')
django.setup()

from django.conf import settings
from blog.models import Post
from django.core.files import File
from django.core.files.storage import default_storage
from storages.backends.azure_storage import AzureStorage
import shutil

def migrate_images():
    print("🚀 Starting image migration to Azure Blob Storage...")
    
    # Initialize Azure Storage
    azure_storage = AzureStorage()
    
    # Get all posts with featured images
    posts_with_images = Post.objects.filter(featured_image__isnull=False)
    print(f"Found {posts_with_images.count()} posts with images")
    
    migrated_count = 0
    error_count = 0
    
    for post in posts_with_images:
        try:
            image_name = post.featured_image.name
            local_path = os.path.join(settings.MEDIA_ROOT, image_name)
            
            print(f"\n📄 Processing: {post.title[:50]}...")
            print(f"  Image: {image_name}")
            
            # Check if file exists locally
            if os.path.exists(local_path):
                print(f"  ✅ Local file exists: {local_path}")
                
                # Check if already exists in Azure
                try:
                    azure_storage.url(image_name)
                    # If we get here, file exists in Azure
                    if azure_storage.exists(image_name):
                        print(f"  ℹ️  Already in Azure, skipping...")
                        continue
                except:
                    pass  # File doesn't exist in Azure, need to upload
                
                # Upload to Azure
                with open(local_path, 'rb') as f:
                    file_obj = File(f)
                    azure_path = azure_storage.save(image_name, file_obj)
                    print(f"  ✅ Uploaded to Azure: {azure_path}")
                    migrated_count += 1
                    
            else:
                print(f"  ❌ Local file not found: {local_path}")
                # Clear the image field if local file doesn't exist
                post.featured_image = None
                post.save()
                print(f"  🧹 Cleared image field for post")
                error_count += 1
                
        except Exception as e:
            print(f"  ❌ Error processing {post.title[:50]}: {e}")
            error_count += 1
    
    print(f"\n🎉 Migration completed!")
    print(f"  ✅ Migrated: {migrated_count} images")
    print(f"  ❌ Errors: {error_count} images")
    
    # Test a few URLs
    print(f"\n🔍 Testing migrated image URLs...")
    test_posts = Post.objects.filter(featured_image__isnull=False)[:3]
    for post in test_posts:
        print(f"  {post.title[:30]}: {post.featured_image.url}")

if __name__ == "__main__":
    migrate_images()