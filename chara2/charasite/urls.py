from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name ='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView, name='book_detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my_borrowed'),
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew_book_librarian'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView, name='author_detail'),
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView, name='project_detail'),
    url(r'^chapter/(?P<pk>\d+)$', views.ChapterDetailView, name='chapter_detail'),
    url(r'^articles/$', views.ArticleListView.as_view(), name='articles'),
    url(r'^article/(?P<pk>\d+)$', views.ArticleDetailView, name='article_detail'),
    url(r'^projects/create/$', views.ProjectCreationView, name='project_creation'),
    url(r'^project/createchapter/$', views.ChapterCreationView, name='chapter_creation'),
]
