from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Category, Blog


def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-updated_at')
    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'posts': posts
    }
    return render(request, 'blogs/home.html', context)


def posts_by_category(request, cat_id):    
    posts = Blog.objects.filter(category=cat_id, status='Published')    
    try:
        category = get_object_or_404(Category, id=cat_id)
    except Http404:        
        return render(request, 'blogs/404.html')    
    context = {'posts': posts, 'category': category}
    return render(request, 'blogs/posts_by_category.html', context)