#!/usr/bin/env python3
"""
Check Azure Blob Storage configuration in production
Create this as a Django management command or simple view
"""

# Add this to views.py temporarily for debugging
def debug_storage_settings(request):
    from django.conf import settings
    from django.http import HttpResponse
    import json
    
    debug_info = {
        'DEBUG': settings.DEBUG,
        'USE_AZURE_STORAGE': getattr(settings, 'USE_AZURE_STORAGE', 'NOT SET'),
        'MEDIA_URL': settings.MEDIA_URL,
        'DEFAULT_FILE_STORAGE': getattr(settings, 'DEFAULT_FILE_STORAGE', 'Default Django'),
        'AZURE_ACCOUNT_NAME': getattr(settings, 'AZURE_ACCOUNT_NAME', 'NOT SET'),
        'AZURE_CONTAINER': getattr(settings, 'AZURE_CONTAINER', 'NOT SET'),
    }
    
    return HttpResponse(
        f"<pre>{json.dumps(debug_info, indent=2)}</pre>",
        content_type='text/html'
    )