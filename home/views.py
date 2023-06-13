from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tag, Category, Blog
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    # Retrieve the latest 5 posts from the database
    post = Post.objects.order_by('-dateTimepublishedby')[:5]

    # Retrieve the three most interactive posts
    interactive_posts = Post.objects.annotate(num_likes=Count('liked_by'), num_comments=Count('commented_by')).order_by('-num_likes', '-num_comments')[:3]

    # Retrieve the 8 most frequently used tags
    popular_tags = Tag.objects.annotate(tag_count=Count('post')).order_by('-tag_count')[:8]

    # Retrieve the six most frequently used categories
    categories = Category.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:6]

    context = {
        'post': post,
        'interactive_posts': interactive_posts,
        'popular_tags': popular_tags,
        'categories': categories
    }
    return render(request, 'home/home.html', context)

def post(request):
    # Retrieve all posts from the database
    all_posts = Post.objects.all()

    # Set the number of posts to display per page
    posts_per_page = 10

    # Create a Paginator object
    paginator = Paginator(all_posts, posts_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    posts = Post.objects.all()
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, 'home/posts.html', context)

def search_results(request):
    query = request.GET.get('q')
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query) |
            Q(dateTimepublishedby__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.none()
    
    return render(request, 'home/search_results.html', {'posts': posts, 'query': query})

def category_filter_results(request):
    category_id = request.GET.get('category_id')
    
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            posts = Post.objects.filter(category=category)
        except Category.DoesNotExist:
            posts = []
    else:
        posts = Post.objects.all()
    
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
    }
    
    return render(request, 'home/search_results.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')

        # Update the user profile with the new details
        user = request.user
        user.username = username
        user.email = email
        if avatar:
            user.avatar = avatar
        user.save()

        return redirect('profile')  # Redirect to the profile page after saving

    return render(request, 'profile.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Authentication failed, display an error message
            error_message = 'Invalid username or password.'
            return render(request, 'home/login.html', {'error_message': error_message})
    else:
        return render(request, 'home/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login') 

def blog_details(request, blog_id):
    blog = get_object_or_404(Post, pk=blog_id)
    return render(request, 'home/blog_details.html', {'blog': blog})