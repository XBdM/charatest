from .models import Project, Chapter
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def listproj_context_processor(request):
    return {
        'listproj': Project.objects.filter(is_published=True),
    }

def listnewchapter_context_processor(request):
    return {
        'listnewchap': Chapter.objects.filter(is_published=True).order_by('-date_of_last_edit')[:3],
    }