# CivicBlogs - Django Blog Platform

## Project Overview

CivicBlogs เป็นแพลตฟอร์มสำหรับเขียนบล็อกที่ใช้ Django Framework พร้อมการเชื่อมต่อ Supabase PostgreSQL Database

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: Supabase PostgreSQL
- **Frontend**: Tailwind CSS + Django Templates
- **Rich Text Editor**: CKEditor 4
- **Image Processing**: Pillow
- **Authentication**: Django built-in auth
- **Tags**: django-taggit

## Project Structure

```
civicblogs/
├── civicblogs/              # Main Django project
│   ├── settings.py          # Configuration with Supabase integration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── blog/                   # Main blog application
│   ├── models.py           # Django models (Category, Post, etc.)
│   ├── views.py            # Blog views and logic
│   ├── urls.py             # Blog URL patterns
│   ├── admin.py            # Django admin configuration
│   ├── supabase_backend.py # Supabase REST API integration
│   └── migrations/         # Database migrations
├── templates/              # HTML templates
│   ├── blog/              # Blog-specific templates
│   └── admin/             # Admin interface customization
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files (images)
├── .env                   # Environment variables
└── manage.py              # Django management commands
```

## Database Architecture

### Data Storage Strategy
- **Structured Data**: Stored in Supabase PostgreSQL
- **Media Files**: Stored locally in `media/` directory
- **Static Files**: Served from `static/` directory

### Django Models

#### Category Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Post Model
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    excerpt = models.TextField(max_length=300, blank=True)
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to=upload_featured_image)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    tags = TaggableManager(blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Database Tables (in Supabase)
- `blog_category` - Categories
- `blog_post` - Blog posts
- `auth_user` - Users
- `taggit_tag` - Tags
- `taggit_taggeditem` - Tag relationships

## Supabase Integration

### Connection Configuration
```python
# .env file
USE_POSTGRES=True
DATABASE_URL=postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres
SUPABASE_URL=https://beeydumbrvtrllpmmlos.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Dual Database Support
```python
# settings.py - Flexible database configuration
USE_POSTGRES = config('USE_POSTGRES', default=False, cast=bool)

if USE_POSTGRES:
    # Supabase PostgreSQL
    DATABASE_URL = config('DATABASE_URL')
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    # SQLite fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

## Admin Interface

### Access
- URL: `http://127.0.0.1:8000/admin/`
- Categories: `http://127.0.0.1:8000/admin/blog/category/`
- Posts: `http://127.0.0.1:8000/admin/blog/post/`

### Admin User
- Email: `evo_reaction@hotmail.com`
- Password: `YY_12345`

## Development Workflow

### Common Commands

#### Server Management
```bash
# Start development server
python3 manage.py runserver 127.0.0.1:8000

# Run migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser
```

#### Database Operations
```bash
# Make migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Database shell
python3 manage.py shell
```

#### Data Management
```bash
# Load sample data
python3 manage.py populate_sample_data

# Export data
python3 manage.py dumpdata > backup.json

# Import data
python3 manage.py loaddata backup.json
```

### Testing Database Connection
```bash
# Test Supabase connection
python3 connect_supabase_test.py

# Test Django database
python3 manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print('Connection OK')"
```

## File Upload System

### Image Storage
```python
# Featured images stored locally
def upload_featured_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('blog/featured_images', filename)
```

### Storage Locations
- **Development Images**: `/Applications/MAMP/htdocs/civicblogs/media/blog/featured_images/`
- **Production Images**: Azure Blob Storage (`civicblogs12/media`)
- **CKEditor uploads**: `/Applications/MAMP/htdocs/civicblogs/media/uploads/`
- **Image metadata**: Stored in Supabase database

## API Integration

### Supabase Backend Class
```python
# blog/supabase_backend.py
class SupabaseBackend:
    def create_post(self, data)    # Create new post
    def get_posts(self, status)    # Get posts by status
    def get_categories(self)       # Get all categories
    def search_posts(self, query)  # Search functionality
```

## Security Features

### Row Level Security (RLS)
- Comprehensive RLS policies in `supabase_schema.sql`
- Role-based access control
- Secure API endpoints

### Environment Variables
```bash
# Development (.env)
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
USE_POSTGRES=True
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJ...

# Azure Blob Storage (Production)
USE_AZURE_STORAGE=True
AZURE_STORAGE_ACCOUNT_NAME=civicblogs12
AZURE_STORAGE_ACCOUNT_KEY=[Your Azure Storage Account Key]
AZURE_STORAGE_CONTAINER_NAME=media
```

## Troubleshooting

### Database Connection Issues
1. Check `.env` file configuration
2. Verify Supabase credentials
3. Test network connectivity
4. Use SQLite fallback if needed

### Server Startup Issues
1. Check for port conflicts
2. Verify database connection
3. Run migrations if needed
4. Check for missing dependencies

## Design System

### Color Palette (Tailwind CSS)
- **Primary Yellow**: #f59e0b (yellow-500)
- **Light Yellow**: #fef3c7 (yellow-100)
- **Dark Yellow**: #d97706 (yellow-600)
- **Yellow Accent**: #fbbf24 (yellow-400)
- **Gray Scales**: gray-50 to gray-900
- **White**: #ffffff
- **Black**: #000000

### Typography (Tailwind CSS)
- **Primary Font**: 'Kanit', system-ui, sans-serif
- **Font Weights**: 
  - Regular: 400 (font-normal)
  - Medium: 500 (font-medium)
  - Semibold: 600 (font-semibold)
  - Bold: 700 (font-bold)
- **Text Sizes**: text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl, text-4xl

### Modern Design Features
- **Glass Effects**: backdrop-blur-sm/md with transparency
- **Rounded Corners**: rounded-lg, rounded-xl, rounded-2xl
- **Shadows**: shadow-sm, shadow-lg, shadow-xl
- **Transitions**: transition-all duration-200/300
- **Hover Effects**: hover:scale-105, hover:-translate-y-1
- **Grid Layouts**: grid-cols-1 md:grid-cols-2 lg:grid-cols-3

## Current Status

### ✅ Completed Features
- Django project setup with Supabase integration
- Blog models (Category, Post, Tags, Newsletter, Contact)
- **Comment system removed** - No longer using comments
- Admin interface configuration with custom yellow-black-white theme
- User authentication
- Image upload system (local storage)
- Sample data population
- Flexible database configuration
- **Complete Tailwind CSS Migration** - Replaced Bootstrap entirely
- **Modern Professional Design** - Clean, comfortable user experience
- **Responsive Design** - Mobile-first approach with all screen sizes
- **Interactive Elements** - Smooth animations and hover effects

### 🎨 Latest Design Updates (September 2025)
- **✅ Tailwind CSS Integration**: Complete migration from Bootstrap to Tailwind CSS
- **✅ Modern Homepage**: Professional hero section with gradient backgrounds
- **✅ Card-based Layout**: Featured posts with hover effects and image overlays
- **✅ Professional Sidebar**: Categories, tags, and recent posts widgets
- **✅ Enhanced Navigation**: Glass effects with backdrop blur
- **✅ Modern Typography**: Kanit font with proper hierarchy
- **✅ Responsive Grid**: CSS Grid and Flexbox for all screen sizes
- **✅ Interactive Elements**: Smooth transitions and micro-interactions
- **✅ SVG Icons**: Custom SVG icons for better performance
- **✅ Glass Effects**: Modern backdrop-blur and transparency effects
- **✅ Professional Color Palette**: Refined yellow theme with proper contrast

### 🔄 Data Storage Verification
- **Categories**: 7 items in Supabase
- **Posts**: 2 items in Supabase  
- **Users**: 1 admin user in Supabase
- **Newsletter**: Active subscription system
- **Comments**: ❌ Removed (not used)
- **Images**: Stored locally in media/ directory

### 📝 Admin Interface Locations
- Category management: `http://127.0.0.1:8000/admin/blog/category/`
- Post management: `http://127.0.0.1:8000/admin/blog/post/`
- User management: `http://127.0.0.1:8000/admin/auth/user/`

## Frontend Architecture

### Template Structure
```
templates/
├── base.html                    # Base template with Tailwind CSS
├── blog/
│   ├── post_list.html          # Homepage with modern design
│   ├── post_detail.html        # Post detail page
│   └── category_list.html      # Category listing
└── admin/
    └── css/admin.css           # Admin interface styling
```

### Key Template Features
- **Responsive Design**: Mobile-first approach
- **Component-based**: Reusable UI components
- **Performance**: Lazy loading and optimized images
- **Accessibility**: Proper ARIA labels and keyboard navigation
- **SEO**: Meta tags and semantic HTML

### JavaScript Enhancements
- Smooth scrolling for anchor links
- Enhanced navbar scroll effects
- Lazy loading for images
- Interactive hover animations
- Search functionality improvements

## Development Commands

### Frontend Development
```bash
# Start development server with external access
python3 manage.py runserver 0.0.0.0:8000

# Access the website
http://localhost:8000/

# Admin interface
http://localhost:8000/admin/
```

### Database Commands
```bash
# Check database connection
python3 manage.py shell -c "from django.db import connection; print('Database:', connection.vendor)"

# Run migrations
python3 manage.py migrate

# Create sample data
python3 manage.py shell -c "from blog.models import Category, Post; print('Categories:', Category.objects.count(), 'Posts:', Post.objects.count())"
```

## Deployment Architecture

### Azure Cloud Infrastructure
- **Web App**: civicspace (Azure App Service)
- **Storage**: civicblogs12 (Azure Blob Storage)  
- **Database**: Supabase PostgreSQL (External)
- **Resource Group**: civicspace_group
- **Region**: Southeast Asia

### Deployment Pipeline
- **Source Control**: GitHub (cabindev/civicblogs)
- **CI/CD**: GitHub Actions
- **Auto-Deploy**: Trigger on push to main branch
- **Environment**: Production with auto-scaling

### Azure Blob Storage Configuration
```python
# Production media storage
if not DEBUG and config('USE_AZURE_STORAGE', default=False, cast=bool):
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_ACCOUNT_NAME = 'civicblogs12'
    AZURE_CONTAINER = 'media'
    AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'
```

### Production URLs
- **Website**: https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net
- **Admin**: https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/admin
- **Media Storage**: https://civicblogs12.blob.core.windows.net/media/

## Next Steps

1. ✅ **Tailwind CSS Migration** - Completed
2. ✅ **Professional Homepage Design** - Completed  
3. ✅ **Responsive Layout** - Completed
4. ✅ **Azure Deployment** - Completed
5. ✅ **Azure Blob Storage** - Configured for media files
6. ✅ **GitHub Actions CI/CD** - Auto-deploy pipeline active
7. 🔄 **Test Media Upload** - Verify Azure Blob Storage integration
8. 🔄 **Post Detail Page** - Update with Tailwind CSS
9. 🔄 **Category Pages** - Create with new design
10. 🔄 **Search Functionality** - Implement backend search

---

**Last Updated**: September 8, 2025  
**Django Version**: 5.2.5  
**Database**: Supabase PostgreSQL  
**Frontend**: Tailwind CSS (Migrated from Bootstrap)  
**Deployment**: Azure App Service with GitHub Actions  
**Storage**: Azure Blob Storage for media files  
**Status**: Production Deployed ✅  
**Design Status**: Modern Professional UI Complete ✅