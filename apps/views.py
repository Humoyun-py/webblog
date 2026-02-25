from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Category, Blog, Comment, Profile
from .forms import ProfileForm, BlogForm


def home_page(request):
    blogs = Blog.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Search and filter functionality
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        blogs = blogs.filter(title__icontains=search_query)
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'blog.html', context)

# Blog list page
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        blogs = blogs.filter(title__icontains=search_query)
    
    if category_id:
        blogs = blogs.filter(category_id=category_id)
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'blog.html', context)

# Blog detail page
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comment_set.all().order_by('-created_at')
    categories = Category.objects.all()
    
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            content = request.POST.get('comment', '')
            if content:
                Comment.objects.create(
                    content=content,
                    author=user,
                    blog=blog
                )
                messages.success(request, 'Comment added successfully!')
                return redirect('blog_detail', pk=pk)
        else:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('blog_detail', pk=pk)
    
    context = {
        'blog': blog,
        'comments': comments,
        'categories': categories,
    }
    return render(request, 'blog_detail.html', context)

# Categories page
def categories_page(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'categories.html', context)

# Category detail page
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    blogs = Blog.objects.filter(category=category).order_by('-created_at')
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'category': category,
        'blogs': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'blog.html', context)

# Contact page
def contact_page(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # You can save this to a database or send an email
        if name and email and subject and message:
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    context = {
        'categories': categories,
    }
    return render(request, 'contact.html', context)

# Register page
def register(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        
        # Validate inputs
        if not username or not email or not password or not password2:
            messages.error(request, 'Please fill in all fields.')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return redirect('register')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    
    context = {
        'categories': categories,
    }
    return render(request, 'register.html', context)

# Login page
def login_view(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    context = {
        'categories': categories,
    }
    return render(request, 'login.html', context)

# Logout page
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')



@login_required
def profile(request):
    # profile = request.user.profile   # allaqachon mavjud bo'lsa
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')   # yoki 'profile' nomli url ga
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
        'user_blogs': user_blogs,
        'categories': categories,
    }
    return render(request, 'profile.html', context)


@login_required
def create_blog(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog muvaffaqiyatli yaratildi!')
            return redirect('profile')
        else:
            messages.error(request, 'Formada xatolik mavjud.')
    else:
        form = BlogForm()
    
    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'create_blog.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    user_blogs = Blog.objects.filter(author=user).order_by('-created_at')
    categories = Category.objects.all()
    
    context = {
        'profile': profile,
        'user': user,
        'user_blogs': user_blogs,
        'is_own_profile': request.user == user,
        'categories': categories,
    }
    return render(request, 'user_profile.html', context)
