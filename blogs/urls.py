from django.urls import path
from . import views


urlpatterns = [    
    path('', views.home, name='home'),
    path('category/<int:cat_id>/', views.posts_by_category, name='posts_by_category'),
    path('blogs/<slug:slug>/', views.single_blog, name='single_blog'),
    path('blogs/search/', views.search, name='search'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]