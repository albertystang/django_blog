import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from blogs.models import Category, Blog
from .forms import CategoryForm, BlogPostForm


@login_required
def dashboard(request):
    cat_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()
    context = {'cat_count': cat_count, 'blog_count': blog_count}
    return render(request, 'dashboards/dashboard.html', context)


@login_required
def categories(request):    
    return render(request, 'dashboards/categories.html')


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The category has been added...')            
            return redirect('categories')
    return render(request, 'dashboards/add_category.html', {'form': form})


@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'The category has been updated...')
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {'form': form, 'category': category}
    return render(request, 'dashboards/edit_category.html', context)


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'The category has been deleted...')
    return redirect('categories')


@login_required
def posts(request):
    posts = Blog.objects.all().order_by('-updated_at')
    context = {'posts': posts}
    return render(request, 'dashboards/posts.html', context)


@login_required
def add_post(request):
    form = BlogPostForm()
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            title = form.cleaned_data['title']                       
            post.slug = slugify(title) + '-' + str(uuid.uuid4())
            post.save()
            messages.success(request, 'The post has been added...')
            return redirect('posts')
    return render(request, 'dashboards/add_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Blog, id=pk)    
    form = BlogPostForm(instance=post)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)            
            title = form.cleaned_data['title']                       
            post.slug = slugify(title) + '-' + str(uuid.uuid4())
            post.save()
            messages.success(request, 'The post has been updated...')
            return redirect('posts')
    context = {'post': post, 'form': form}
    return render(request, 'dashboards/edit_post.html', context)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Blog, id=pk)    
    post.delete()
    messages.success(request, 'The post has been deleted...')
    return redirect('posts')