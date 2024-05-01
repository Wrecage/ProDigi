from django.shortcuts import render,get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse

import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from app1.tasks import send_reminder_notification


from .models import Task
from .forms import TaskForm
from django.db.models import Q
# from .decorators import prevent_logged_in_users
#@login_required(login_url='login')
from django.views.decorators.http import require_POST



#languageTool
import language_tool_python




from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)

from django.core.exceptions import ValidationError


def IndexPage(request):
  return render(request,'index.html')


def HomePage(request):
  return render(request,'home.html')


def SignupPage(request):
    message = None
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')

        validators = [
            UserAttributeSimilarityValidator(),
            MinimumLengthValidator(min_length=8),
            CommonPasswordValidator(),
            NumericPasswordValidator()
        ]

        try:
            for validator in validators:
                validator.validate(pass1)
        except ValidationError as error:
            message = ", ".join(error.messages)
            return render(request, 'signup.html', {'message': message})

        if User.objects.filter(username=uname).exists():
            message = "Username already taken"
        else:
            my_user = User.objects.create_user(uname, password=pass1)
            my_user.save()
            return redirect('login')   
    return render(request, 'signup.html', {'message': message})
    


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            error_message = "Account not registered"
            return render(request, 'login.html', {'message': error_message})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error_message = "Incorrect username or password"
            return render(request, 'login.html', {'message': error_message})

    return render(request, 'login.html')

@login_required
def ProfilePage(request):
    diary_entry_count = DiaryEntry.objects.filter(user=request.user).count()
    task_count = Task.objects.filter(user=request.user).count()

    username = request.user.username
    
    return render(request, 'profile.html', {'diary_entry_count': diary_entry_count, 'task_count': task_count,'username': username})


def LogoutPage(request):
    logout(request)
    return redirect('index')





#apply suggestions
def apply_suggestions(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')

        tool = language_tool_python.LanguageTool('en-US')
        corrected_text = tool.correct(text)
        tool.close()

        return JsonResponse({'text': corrected_text})

    return JsonResponse({'error': 'Invalid request'})




#diary entry
@login_required
def diary_entries(request):
    sort = request.GET.get('sort', 'date')  
    if sort == 'date':
        entries = DiaryEntry.objects.order_by('date')
    elif sort == 'title':
        entries = DiaryEntry.objects.order_by('title')
    else:
        entries = DiaryEntry.objects.all()
    if request.method == 'POST':
        diary_form = DiaryEntryForm(request.POST, user=request.user)

        if diary_form.is_valid():
            diary = diary_form.save(commit=False)
            diary.user = request.user 
            diary.save()
            
            return redirect('diary_entries')
            
    else:
       diary_form = DiaryEntryForm()

    return render(request, 'diary_entry_form.html', {'entries': entries, 'diary_form': diary_form})


@login_required
def edit_entry(request, id):
    entry = get_object_or_404(DiaryEntry, pk=id)
    form = DiaryEntryForm(request.POST or None, instance=entry, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('diary_entries')
    return render(request, 'edit_entry.html', {'form': form})

 



@login_required
def delete_entry(request,id):
    entry = get_object_or_404(DiaryEntry, pk=id)
    entry.delete()
    return redirect('diary_entries')



#Task Mangement
@login_required
def task_list(request):
    sort_option = request.GET.get('sort', None)
    category_filter = request.GET.get('category', None) 
    tasks = Task.objects.all()

    if category_filter:
        tasks = tasks.filter(category=category_filter)
    
    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if sort_option == 'completed':
        tasks = tasks.filter(completed=True)
    elif sort_option == 'pending':
        tasks = tasks.filter(completed=False)

    return render(request, 'task_list.html', {'tasks': tasks, 'sort_option': sort_option, 'query': query})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    # Check if editing mode is requested
    editing = request.GET.get('editing', False)

    if editing:
        form = TaskForm(request.POST or None, instance=task, user=request.user)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = None

    return render(request, 'task_detail.html', {'task': task, 'form': form, 'editing': editing})

@login_required
def add_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST, user=request.user)

        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user  
            task.save()
            return redirect('task_list')
    else:
       task_form = TaskForm()
    return render(request, 'add_task.html', {'task_form': task_form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('task_list')



def grammar_check_view(request):
    return render(request, 'grammar_check_form.html')