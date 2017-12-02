from django.contrib.auth.decorators import permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from .models import *
import datetime

from .forms import *

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Project.objects.all().count()
    num_instances=Chapter.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=Chapter.objects.all().count()
    num_authors=User.objects.count()  # The 'all()' is implied by default.
    
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,'num_visits':num_visits},
    )
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Charasite Account'
            message = render_to_string('account_activation_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': str(urlsafe_base64_encode(force_bytes(user.pk)))[2:-1],
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(subject, message, to =[form.cleaned_data.get('email')])
            email.send()
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'charasite/signup.html', context={'form': form,})
    
        
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')



class ProjectListView(generic.ListView):
    model = Project
    paginate_by = 10
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)
    

def ProjectDetailView(request,pk):
    try:
        project_id=Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")

    #book_id=get_object_or_404(Book, pk=pk)

    list_chap = Chapter.objects.filter(project=project_id).filter(is_published = True).order_by('number')
    comments = CommentProject.objects.all().filter(project=project_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            commentaire = CommentProject(project=project_id, author=request.user, content=form.cleaned_data['content'])
            commentaire.save()
            comments = CommentProject.objects.all().filter(project=project_id)
            return render(request, 'charasite/project_detail.html',
                          context={'project':project_id, 'list_chapter':list_chap, 'form': form, 'comments': comments})
    else:
        form = CommentForm()
    return render(
        request,
        'charasite/project_detail.html',
        context={'project':project_id,'list_chapter':list_chap, 'form': form, 'comments': comments}
    )
    
def ChapterDetailView(request,pk):
    try:
        chapter_id=Chapter.objects.get(pk=pk)
    except Chapter.DoesNotExist:
        raise Http404("Chapter does not exist")
    
    if (not chapter_id.is_published):
        raise Http404("Chapter does not exist")
    
    comments = CommentChapter.objects.all().filter(chapter = chapter_id)
    
    #formulaire
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST)

        if form.is_valid():
            commentaire = CommentChapter(chapter = chapter_id, author = request.user, content=form.cleaned_data['content'])
            commentaire.save()
            comments = CommentChapter.objects.all().filter(chapter = chapter_id)
            return render(request, 'charasite/chapter_detail.html',context={'chapter':chapter_id,'form':form,'comments':comments})
    
    else:
        form = CommentForm()

    return render(request, 'charasite/chapter_detail.html',context={'chapter':chapter_id,'form':form,'comments':comments})

    
    return render(
        request,
        'charasite/chapter_detail.html',
        context={'chapter':chapter_id,'comments':comments,}
    )
    
def ArticleDetailView(request,pk):
    try:
        article_id=Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    
    if (not article_id.is_published):
        raise Http404("Article does not exist")
        
    comments = CommentArticle.objects.all().filter(article = article_id)
    
    #formulaire
        
    if request.method == 'POST':
    
        form = CommentForm(request.POST)

        if form.is_valid():
            commentaire = CommentArticle(article = article_id, author = request.user, content=form.cleaned_data['content'])
            commentaire.save()
            comments = CommentArticle.objects.all().filter(article = article_id)
            return render(request, 'charasite/article_detail.html',context={'article':article_id,'form':form,'comments':comments})
    
    else:
        form = CommentForm()
    
    return render(request, 'charasite/article_detail.html',context={'article':article_id,'form':form,'comments':comments})

class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 3


def ProjectCreationView(request):
    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            newProject = form.save()
            return render(request, 'charasite/project_creation_form.html', {'form': form, 'is_saved': True})
    else:
        form = ProjectCreationForm()

    return render(request, 'charasite/project_creation_form.html', {'form': form, 'is_saved': False})

def ChapterCreationView(request):
    if request.method == 'POST':
        form = ChapterCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'charasite/chapter_creation_form.html', {'form': form, 'is_saved': True})
    else:
        form = ChapterCreationForm()

    return render(request, 'charasite/chapter_creation_form.html', {'form': form, 'is_saved': False})

def ChapterEditView(request, pk):
    chap = get_object_or_404(Chapter, id=pk)
    
    if request.method == 'POST':
        form = ChapterCreationForm(request.POST, instance=chap)
        if form.is_valid():
            chap.body =  request.POST.get('body')
            chap.save()
            return render(request, 'charasite/chapter_edit_form.html', {'form': chap, 'is_saved': True, 'repository':chap.repository,})
    else:
        form = ChapterCreationForm(instance=chap)
    return render(request, 'charasite/chapter_edit_form.html', {'form': form, 'is_saved': True, 'repository':chap.repository,})

def search(request):
    query_string = ''
    found_entries = None
    if (request.GET):
        query_string = request.GET.get('search_box')
        project_entries_found = Project.objects.filter(name__icontains=query_string).order_by('id')
        ## Permettra une recherche étendue au utilisateur une fois la fonction signin établie.
        # found_entries = User.objects.filter(first_name__icontains=query_string).order_by('id')
        # found_entries2 = User.objects.filter(last_name__icontains=query_string).order_by('id')
        # user_entries_found = found_entries | found_entries2
        return render(request, 'charasite/search_results.html',
                              { 'query_string': query_string, 'project_entries_found': project_entries_found } )
    return render(request, 'charasite/search_results.html')

def search_page(request):
    return render(request, 'charasite/search_page.html')

def ArborescenceEditView(request,pk):
    try:
        repository_id=Repository.objects.get(pk=pk)
    except Repository.DoesNotExist:
        raise Http404("Article does not exist")
    
    if request.user.is_authenticated:    
    
        if TeamMember.objects.filter(member=request.user).filter(team=repository_id.project).exists():
        
            repo_repo_children = Repository.objects.filter(parent_repository = repository_id).order_by('name')
            repo_chap_children = Chapter.objects.filter(repository = repository_id).order_by('number')
        
            return render(request, 'charaedit/arborescence.html', {'repository':repository_id, 'repo_repo_children':repo_repo_children,'repo_chap_children':repo_chap_children,})
            
        else:
        
            return render(request, 'charaedit/not_authorize.html')
            
    else:
    
        return render(request, 'not_authenticated.html')

def PersonalArborescenceEditView(request,pk):
    try:
        repository_id=Personal_repository.objects.get(pk=pk)
    except Personal_repository.DoesNotExist:
        raise Http404("Repository does not exist")
    
    if request.user.is_authenticated:    
    
        if repository_id.owner == request.user:
        
            repo_prepo_children = Personal_repository.objects.filter(parent_repository = repository_id).order_by('name')
            repo_repo_children = repository_id.repositories.order_by('name')
            repo_proj_children = repository_id.projects.order_by('name')
            repo_chap_children = repository_id.chapters.order_by('number')
        
            return render(request, 'charaedit/perso_arborescence.html', {'repository':repository_id, 'repo_repo_children':repo_repo_children,'repo_prepo_children':repo_prepo_children,'repo_proj_children':repo_proj_children,'repo_chap_children':repo_chap_children,})
            
        else:
        
            return render(request, 'charaedit/not_authorize.html')
            
    else:
    
        return render(request, 'not_authenticated.html')