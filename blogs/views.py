from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Blog
from assignments.models import About
from .forms import RegistrationForm


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


def register_user(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()            
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have registered successfully...')
                return redirect('home')
            else:
                messages.success(request, ("There was an error in registering, please try again..."))
                return redirect('register')
    return render(request, 'blogs/register.html', {'form': form})


def login_user(request):
    form = AuthenticationForm()    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully...')
                return redirect('home')
            else:                
                messages.success(request, 'There was an error in loggin in. Please try again...')            
        else:
            messages.success(request, 'There was an error in filling out the login form. Please try again...')   
    return render(request, 'blogs/login.html', {'form': form})        
        

def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully...')
    return redirect('home')