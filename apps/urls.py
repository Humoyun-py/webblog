from django.urls import path
from .views import (
    home_page, 
    blog_list, 
    blog_detail, 
    categories_page, 
    category_detail, 
    contact_page,
    profile,
    user_profile,
    create_blog,
    register,
    login_view,
    logout_view
)
from apps import views

urlpatterns = [
    path('', home_page, name='home'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<int:pk>/', blog_detail, name='blog_detail'),
    path('blog/create/', create_blog, name='create_blog'),
    path('categories/', categories_page, name='categories'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('contact/', contact_page, name='contact'),
    path('profile/', profile, name='profile'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]