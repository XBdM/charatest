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
from django.http import HttpResponseRedirect
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
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    
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


    
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

def BookDetailView(request,pk):
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
    return render(
        request,
        'charasite/book_detail.html',
        context={'book':book_id,}
    )
    
def AuthorDetailView(request,pk):
    try:
        author_id=Author.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
    return render(
        request,
        'charasite/author_detail.html',
        context={'author':author_id,}
    )
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='charasite/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        
        
@permission_required('charasite.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all_borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'charasite/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('index')
    
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
            return render(request, 'charasite/chapter_detail.html',
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
            form.save()
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