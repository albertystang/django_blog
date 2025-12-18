from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from .models import Category, Blog
from assignments.models import About


def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-updated_at')
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about
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


def single_blog(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    return render(request, 'blogs/single_blog.html', {'single_blog': single_blog})


def search(request):
    query = request.GET.get('query')    
    blogs = Blog.objects.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(blog_body__icontains=query), status='Published')  
    context = {
        'blogs': blogs,
        'keyword': query,
    }
    return render(request, 'blogs/search.html', context)
    