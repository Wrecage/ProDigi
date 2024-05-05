from django.db import models
from django.contrib.auth.models import User



class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    mood = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    reminder_date = models.DateField(null=True, blank=True)
    reminder_time = models.TimeField(null=True, blank=True)



class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    category = models.CharField(max_length=50, blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    
def __str__(self):
        return self.title