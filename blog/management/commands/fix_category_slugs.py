from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Category


class Command(BaseCommand):
    help = 'Fix categories with empty slugs'

    def handle(self, *args, **options):
        categories_with_empty_slugs = Category.objects.filter(slug='')
        
        if not categories_with_empty_slugs.exists():
            self.stdout.write('No categories with empty slugs found.')
            return
        
        slug_mapping = {
            'เทคโนโลยี': 'technology',
            'การเมือง': 'politics',
            'สังคม': 'society',
            'สิ่งแวดล้อม': 'environment',
        }
        
        for category in categories_with_empty_slugs:
            self.stdout.write(f'Fixing slug for category: {category.name}')
            
            # Use predefined slug if available
            if category.name in slug_mapping:
                proposed_slug = slug_mapping[category.name]
            else:
                # Create generic slug
                proposed_slug = f"category-{category.id}"
            
            # Ensure slug is valid and unique
            final_slug = slugify(proposed_slug) or f"category-{category.id}"
            
            # Check for uniqueness
            counter = 1
            original_slug = final_slug
            while Category.objects.filter(slug=final_slug).exclude(id=category.id).exists():
                final_slug = f"{original_slug}-{counter}"
                counter += 1
            
            category.slug = final_slug
            category.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Fixed: {category.name} -> {category.slug}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {categories_with_empty_slugs.count()} categories!')
        )