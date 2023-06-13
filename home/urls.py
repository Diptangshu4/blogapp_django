from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.post, name="posts"),
    path('search/', views.search_results, name="search_results"),
    path('searchbycategory/', views.category_filter_results, name="category_filter_results"),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('blogs/<int:blog_id>/', views.blog_details, name='blog_details'),
]