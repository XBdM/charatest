from .models import Project
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def listproj_context_processor(request):
    return {
        'listproj': Project.objects.filter(is_published=True),
    }