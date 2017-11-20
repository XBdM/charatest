from .models import *
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
    
def listcurrentproject_context_processor(request):
    if request.user.is_authenticated:
        return {
            'listcurrentproject': list(set([tm.team for tm in TeamMember.objects.filter(member=request.user)]+[proj for proj in Project.objects.filter(owner=request.user)])),
        }
    return {
        'listcurrentproject': [],
    }

def listpersonalrepositories_context_processor(request):
	if request.user.is_authenticated:
		return{
			'listpersonalrepositories': Personal_repository.objects.filter(owner=request.user),
		}
	return {
		'listpersonalrepositories': [],
	}