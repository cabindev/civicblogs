# CivicBlogs Deployment Status

**Last Deployment Trigger**: 2025-10-02 19:30:00 UTC

## Deployment Information
- **Platform**: Azure App Service
- **URL**: https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net
- **Admin URL**: https://civicspace-gqdcg0dxgjbqe8as.southeastasia-01.azurewebsites.net/admin
- **GitHub Repository**: cabindev/civicblogs
- **Auto-Deploy**: Enabled via GitHub Actions

## Environment Configuration
- **Database**: Supabase PostgreSQL
- **Media Storage**: Azure Blob Storage (civicblogs12)
- **Static Files**: WhiteNoise
- **WSGI Server**: Gunicorn

## Production Settings
- DEBUG=False (in production)
- USE_POSTGRES=True
- USE_AZURE_STORAGE=True
- ALLOWED_HOSTS includes Azure domain

Deploy triggered from local environment.