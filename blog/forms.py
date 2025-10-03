from django import forms
from .models import Newsletter, ContactMessage, Post, Category, PostType


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Your Message'}),
        }


class SimplePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'post_type', 'content', 'featured_image', 'featured_image_alt', 'status', 'tags', 'meta_description']
        # Exclude slug field as it will be generated automatically
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'ชื่อบทความ'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'post_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 10}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'featured_image_alt': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'placeholder': 'คำอธิบายรูปภาพ'}),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'}),
            'meta_description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md', 'rows': 3, 'placeholder': 'คำอธิบายสำหรับ SEO'}),
        }