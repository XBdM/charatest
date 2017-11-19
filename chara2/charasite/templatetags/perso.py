from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from ..models import *

register = template.Library()

def repo_exploration(L):
    if (len(L[1])==0):
        return '<li><a href="{}">{}</a></li>'.format(L[0].get_absolute_url(),escape(L[0].name))
    s = '<li><a href="{}">{}</a></li> \n <ul> \n'.format(L[0].get_absolute_url(),escape(L[0].name))
    for child in L[1]:
        s+=repo_exploration(child)
    s+= "</ul>"
    return s
	
def get_list_children(repository):
    l = (repository,[])
    list_children = Repository.objects.filter(parent_repository=repository)
    for child in list_children:
        l[1].append(get_list_children(child))
    return l

@register.filter(is_safe=True)
def repository_display(repository):
    return mark_safe(repo_exploration(get_list_children(repository)))