from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Avg, Count, Q, F
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from .social_models import SocialPost, PostAnalyticsSummary

@staff_member_required
def social_dashboard(request):
    """แสดง Dashboard สถิติโพสต์โซเชียล"""
    
    # ข้อมูลสรุปทั้งหมด
    total_posts = SocialPost.objects.filter(is_active=True).count()
    total_likes = SocialPost.objects.filter(is_active=True).aggregate(Sum('likes_count'))['likes_count__sum'] or 0
    total_comments = SocialPost.objects.filter(is_active=True).aggregate(Sum('comments_count'))['comments_count__sum'] or 0
    total_shares = SocialPost.objects.filter(is_active=True).aggregate(Sum('shares_count'))['shares_count__sum'] or 0
    
    # โพสต์ล่าสุด 30 วัน
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_posts = SocialPost.objects.filter(
        is_active=True,
        post_date__gte=thirty_days_ago
    ).order_by('-post_date')[:20]
    
    # สถิติแยกตามแพลตฟอร์ม
    platform_stats = []
    for platform_code, platform_name in SocialPost.PLATFORM_CHOICES:
        posts = SocialPost.objects.filter(platform=platform_code, is_active=True)
        if posts.exists():
            platform_stats.append({
                'platform': platform_name,
                'platform_code': platform_code,
                'total_posts': posts.count(),
                'total_likes': posts.aggregate(Sum('likes_count'))['likes_count__sum'] or 0,
                'total_comments': posts.aggregate(Sum('comments_count'))['comments_count__sum'] or 0,
                'total_shares': posts.aggregate(Sum('shares_count'))['shares_count__sum'] or 0,
                'avg_engagement': round(posts.aggregate(
                    avg=Avg(F('likes_count') + F('comments_count') + F('shares_count'))
                )['avg'] or 0, 1)
            })
    
    # โพสต์ยอดนิยม (Top 10)
    top_posts = SocialPost.objects.filter(is_active=True).annotate(
        total_engagement=F('likes_count') + F('comments_count') + F('shares_count')
    ).order_by('-total_engagement')[:10]
    
    context = {
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments, 
        'total_shares': total_shares,
        'total_engagement': total_likes + total_comments + total_shares,
        'recent_posts': recent_posts,
        'platform_stats': platform_stats,
        'top_posts': top_posts,
    }
    
    return render(request, 'social/dashboard.html', context)

@staff_member_required  
def social_posts_table(request):
    """แสดงตารางโพสต์โซเชียล"""
    
    # Filter parameters
    platform = request.GET.get('platform', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', '-post_date')  # Default sort by date
    
    # Base queryset
    posts = SocialPost.objects.filter(is_active=True).annotate(
        total_engagement=F('likes_count') + F('comments_count') + F('shares_count')
    )
    
    # Apply filters
    if platform:
        posts = posts.filter(platform=platform)
    
    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
            posts = posts.filter(post_date__date__gte=date_from_parsed)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
            posts = posts.filter(post_date__date__lte=date_to_parsed)
        except ValueError:
            pass
    
    # Apply sorting
    valid_sorts = ['post_date', '-post_date', 'likes_count', '-likes_count', 
                   'comments_count', '-comments_count', 'shares_count', '-shares_count',
                   'total_engagement', '-total_engagement', 'title']
    if sort_by in valid_sorts:
        posts = posts.order_by(sort_by)
    else:
        posts = posts.order_by('-post_date')
    
    # สถิติสำหรับหน้านี้ (คำนวณก่อน pagination)
    filtered_stats = {
        'total_posts': posts.count(),
        'total_likes': posts.aggregate(Sum('likes_count'))['likes_count__sum'] or 0,
        'total_comments': posts.aggregate(Sum('comments_count'))['comments_count__sum'] or 0,
        'total_shares': posts.aggregate(Sum('shares_count'))['shares_count__sum'] or 0,
    }
    filtered_stats['total_engagement'] = (
        filtered_stats['total_likes'] + 
        filtered_stats['total_comments'] + 
        filtered_stats['total_shares']
    )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 25)  # 25 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # คำนวณ engagement percentage สำหรับแต่ละโพสต์ในหน้าปัจจุบัน
    for post in page_obj:
        if filtered_stats['total_engagement'] > 0:
            post.engagement_percentage = round(
                (post.total_engagement / filtered_stats['total_engagement']) * 100, 1
            )
        else:
            post.engagement_percentage = 0
    
    context = {
        'page_obj': page_obj,
        'filtered_stats': filtered_stats,
        'platforms': SocialPost.PLATFORM_CHOICES,
        'current_filters': {
            'platform': platform,
            'date_from': date_from,
            'date_to': date_to,
            'sort': sort_by,
        }
    }
    
    return render(request, 'social/posts_table.html', context)

@staff_member_required
def social_monthly_report(request):
    """รายงานรายเดือน"""
    
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', '')
    
    try:
        year = int(year)
    except (ValueError, TypeError):
        year = timezone.now().year
    
    # ข้อมูลรายเดือนทั้งหมด
    if month:
        try:
            month = int(month)
            summaries = PostAnalyticsSummary.objects.filter(year=year, month=month)
        except (ValueError, TypeError):
            summaries = PostAnalyticsSummary.objects.filter(year=year)
    else:
        summaries = PostAnalyticsSummary.objects.filter(year=year)
    
    summaries = summaries.order_by('month', 'platform')
    
    # ข้อมูลสำหรับ Chart
    monthly_data = []
    for i in range(1, 13):
        month_summaries = PostAnalyticsSummary.objects.filter(year=year, month=i)
        monthly_data.append({
            'month': i,
            'month_name': ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
                          'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'][i],
            'total_posts': month_summaries.aggregate(Sum('total_posts'))['total_posts__sum'] or 0,
            'total_engagement': (
                (month_summaries.aggregate(Sum('total_likes'))['total_likes__sum'] or 0) +
                (month_summaries.aggregate(Sum('total_comments'))['total_comments__sum'] or 0) +
                (month_summaries.aggregate(Sum('total_shares'))['total_shares__sum'] or 0)
            )
        })
    
    context = {
        'summaries': summaries,
        'monthly_data': monthly_data,
        'current_year': year,
        'current_month': int(month) if month else '',
        'available_years': range(2020, timezone.now().year + 2),
        'months': [
            (1, 'มกราคม'), (2, 'กุมภาพันธ์'), (3, 'มีนาคม'), (4, 'เมษายน'),
            (5, 'พฤษภาคม'), (6, 'มิถุนายน'), (7, 'กรกฎาคม'), (8, 'สิงหาคม'),
            (9, 'กันยายน'), (10, 'ตุลาคม'), (11, 'พฤศจิกายน'), (12, 'ธันวาคม')
        ]
    }
    
    return render(request, 'social/monthly_report.html', context)

