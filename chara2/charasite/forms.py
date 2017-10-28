from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
from .models import *

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=512, help_text="Leave a comment")

    def clean_content(self):
        data = self.cleanded_data['content']
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

    class CommentForm(forms.Form):
        content = forms.CharField(widget=forms.Textarea, max_length=512, help_text="Leave a comment")

        def clean_content(self):
            data = self.cleanded_data['content']
            return data

#this code is an exemple.
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #Check date is not in past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
#end exemple.