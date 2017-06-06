from django.contrib.auth.models import User
from django import forms
from .models import MainCategory, Entry


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']

class CategoryForm(forms.ModelForm):

    class Meta:
        model = MainCategory
        fields = ['name']

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['type', 'value', 'description']
