from django import forms
from django.forms import ModelForm
from .models import Task



class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ["creator", "participants", "is_active"]
        labels = {
            'title': 'Title',
            'description': 'Description',
            "category" : "Category",
            "link" : "Link to Social media or Website",
            "estimated_time_mins" : "Estimated Time (mins)",
            "reward" : "Reward"
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "enter the title of your task"}),
            "description": forms.Textarea(attrs={"class" : "text", "placeholder": "enter a description for your task"}),
            "category": forms.Select(attrs={"class": "choices"}),
            "link": forms.TextInput(attrs={"placeholder": "enter a link to your task"}),
            "estimated_time_mins": forms.NumberInput(attrs={"placeholder": "estimated time to finish the task"}),
            "reward": forms.NumberInput(attrs={"placeholder": "enter the amount you are will to pay per task"}),
        }
