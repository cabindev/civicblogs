from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from taggit.models import Tag
from .models import Post, Category, Newsletter, ContactMessage
try:
    from .models import Video
except ImportError:
    Video = None
from .forms import ContactForm, NewsletterForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('taggit_taggeditem_items')
        ).filter(post_count__gt=0).order_by('-post_count')[:10]
        
        # Add latest videos to homepage (with error handling)
        if Video is not None:
            try:
                context['latest_videos'] = Video.objects.filter(status='published').select_related('author', 'category').order_by('-created_at')[:6]
            except Exception:
                # If Video table doesn't exist yet (migrations not run), use empty list
                context['latest_videos'] = []
        else:
            context['latest_videos'] = []
        
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id)[:3]
        return context


if Video is not None:
    class VideoDetailView(DetailView):
        model = Video
        template_name = 'blog/video_detail.html'
        context_object_name = 'video'
        
        def get_queryset(self):
            return Video.objects.filter(status='published').select_related('author', 'category')
        
        def get_object(self, queryset=None):
            obj = super().get_object(queryset)
            obj.view_count += 1
            obj.save(update_fields=['view_count'])
            return obj
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['related_videos'] = Video.objects.filter(
                category=self.object.category,
                status='published'
            ).exclude(id=self.object.id)[:3]
            return context
else:
    # Dummy view when Video model doesn't exist
    class VideoDetailView(DetailView):
        def get(self, request, *args, **kwargs):
            return HttpResponse("Video feature not available", status=404)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.filter(status='published').select_related('author')
        return context


class TaggedPostsView(ListView):
    model = Post
    template_name = 'blog/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Post.objects.filter(tags__slug=tag_slug, status='published').select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return context


class SearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(excerpt__icontains=query),
                status='published'
            ).select_related('author', 'category').distinct()
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ContactView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class NewsletterSubscribeView(FormView):
    form_class = NewsletterForm
    
    def form_valid(self, form):
        form.save()
        if self.request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})
        messages.success(self.request, 'Successfully subscribed to our newsletter!')
        return redirect('blog:post_list')
    
    def form_invalid(self, form):
        if self.request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'errors': form.errors})
        messages.error(self.request, 'There was an error with your subscription.')
        return redirect('blog:post_list')


class AboutView(TemplateView):
    template_name = 'blog/about.html'


def debug_storage_settings(request):
    """Debug view to check Azure Blob Storage configuration"""
    from django.conf import settings
    from decouple import config
    import json
    
    debug_info = {
        'DEBUG': settings.DEBUG,
        'USE_AZURE_STORAGE': config('USE_AZURE_STORAGE', default=False, cast=bool),
        'MEDIA_URL': settings.MEDIA_URL,
        'DEFAULT_FILE_STORAGE': getattr(settings, 'DEFAULT_FILE_STORAGE', 'Default Django'),
        'AZURE_ACCOUNT_NAME': getattr(settings, 'AZURE_ACCOUNT_NAME', 'NOT SET'),
        'AZURE_CONTAINER': getattr(settings, 'AZURE_CONTAINER', 'NOT SET'),
        'Latest Commit': '4269d82 - Enable Azure Blob Storage for development environment',
    }
    
    # Test Azure Storage
    try:
        if config('USE_AZURE_STORAGE', default=False, cast=bool):
            from storages.backends.azure_storage import AzureStorage
            storage = AzureStorage()
            debug_info['Azure Storage Test'] = 'SUCCESS - AzureStorage initialized'
            debug_info['Test URL'] = storage.url('test.jpg')
        else:
            debug_info['Azure Storage Test'] = 'SKIPPED - USE_AZURE_STORAGE=False'
    except Exception as e:
        debug_info['Azure Storage Test'] = f'ERROR: {str(e)}'
    
    return HttpResponse(
        f"<pre>{json.dumps(debug_info, indent=2)}</pre>",
        content_type='text/html'
    )
