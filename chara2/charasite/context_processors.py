from .models import Project, Chapter, Article
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def listproj_context_processor(request):
    return {
        'listproj': Project.objects.filter(is_published=True).order_by('name'),
    }

def listnewchapter_context_processor(request):
    return {
        'listnewchap': Chapter.objects.filter(is_published=True).order_by('-date_of_last_edit')[:3],
    }

def listnewarticle_context_processor(request):
    return {
        'listnewarticle': Article.objects.filter(is_published=True).order_by('-date_of_last_edit')[:3],
    }