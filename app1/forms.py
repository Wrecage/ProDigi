from django import forms
from .models import DiaryEntry
from .models import Task, Category

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['mood', 'date', 'time', 'title', 'content', 'reminder_date', 'reminder_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reminder_date': forms.DateInput(attrs={'type': 'date'}),
            'reminder_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        # Capture the user information from the kwargs
        user = kwargs.pop('user', None)
        super(DiaryEntryForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user

    def save(self, commit=True):
        # Set the user before saving the form
        self.instance.user = self.user
        return super(DiaryEntryForm, self).save(commit)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class TaskForm(forms.ModelForm):
    
 # Define the choices for the category field
    CATEGORY_CHOICES = [
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('school', 'School'),
    ]

    # Use a regular ChoiceField for the category
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed', 'category']


    def __init__(self, *args, **kwargs):
        # Capture the user information from the kwargs
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user

    def save(self, commit=True):
        # Set the user before saving the form
        self.instance.user = self.user
        return super(TaskForm, self).save(commit)