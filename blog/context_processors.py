from django.db.models import Count, Q
from .models import Category

def global_context(request):
    """Make categories available across all templates"""
    return {
        'global_categories': Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).order_by('name')
    }