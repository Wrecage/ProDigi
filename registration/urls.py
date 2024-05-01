"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from .decorators import prevent_logged_in_users



urlpatterns = [
    #Account    
    path('admin/', admin.site.urls),
    path('', views.IndexPage, name='index'),
    path('home/', views.HomePage, name='home'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('profile/', views.ProfilePage, name='profile'),
    path('logout/', views.LogoutPage, name='logout'),

    # Diary entry related URLs
    path('entry/', views.diary_entries, name='diary_entries'),
    path('entry/delete/<int:id>/', views.delete_entry, name='delete_entry'),
    path('entry/edit/<int:id>/', views.edit_entry, name='edit_entry'),

    #Task Management related URLS
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),


    #Language Tool related URLS
    path('apply_suggestions/', views.apply_suggestions, name='apply_suggestions'),
    path('grammar-check/', views.grammar_check_view, name='grammar_check'),

]
