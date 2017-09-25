from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
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
]
