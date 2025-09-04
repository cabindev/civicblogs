from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post
import re


class Command(BaseCommand):
    help = 'Fix posts with empty slugs'

    def handle(self, *args, **options):
        posts_with_empty_slugs = Post.objects.filter(slug='')
        
        if not posts_with_empty_slugs.exists():
            self.stdout.write('No posts with empty slugs found.')
            return
        
        for post in posts_with_empty_slugs:
            self.stdout.write(f'Fixing slug for post: {post.title}')
            
            # Create slug based on post title and ID
            base_slug = f"post-{post.id}"
            
            # Try to extract English characters from title
            english_part = re.sub(r'[^\w\s-]', '', post.title.lower())
            english_part = re.sub(r'[-\s]+', '-', english_part).strip('-')
            
            if english_part:
                proposed_slug = f"{base_slug}-{english_part[:30]}"
            else:
                # Use transliteration for Thai or create generic slug
                if 'เทคโนโลยี' in post.title:
                    proposed_slug = f"{base_slug}-technology"
                elif 'การเมือง' in post.title:
                    proposed_slug = f"{base_slug}-politics"
                elif 'สิ่งแวดล้อม' in post.title:
                    proposed_slug = f"{base_slug}-environment"
                else:
                    proposed_slug = base_slug
            
            # Ensure slug is valid and unique
            final_slug = slugify(proposed_slug) or base_slug
            
            # Check for uniqueness
            counter = 1
            original_slug = final_slug
            while Post.objects.filter(slug=final_slug).exists():
                final_slug = f"{original_slug}-{counter}"
                counter += 1
            
            post.slug = final_slug
            post.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Fixed: {post.title} -> {post.slug}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {posts_with_empty_slugs.count()} posts!')
        )