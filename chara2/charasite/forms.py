from django import forms
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import *


class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date', )

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=512, help_text="Leave a comment")

    def clean_content(self):
        data = self.cleaned_data['content']
        return data


class ProjectCreationForm(forms.ModelForm):
    #def __init__(self, stat, *args, **kwargs):
        #super(ProjectForm, self).__init__(*args, **kwargs)
    class Meta:
        fields = ('name', 'description', 'is_public', 'owner', 'genre', 'is_published')
        model = Project
    def save(self, commit=True):
        project = super(ProjectCreationForm, self).save(commit=False)
        if commit:
            project.save()
        return project

class ChapterCreationForm(forms.ModelForm):
    #def __init__(self, stat, *args, **kwargs):
        #super(ProjectForm, self).__init__(*args, **kwargs)
    class Meta:
        fields = ('project', 'repository', 'number', 'title', 'prevChapter', 'summary', 'content', 'is_published')
        model = Chapter
    def save(self, commit=True):
        chapter = super(ChapterCreationForm, self).save(commit=False)
        if commit:
            chapter.save()
        return chapter

