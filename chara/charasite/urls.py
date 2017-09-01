from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^books/$', views.BookListView.as_view(), name='books'),
	url(r'^book/(?P<pk>\d+)$', views.BookDetailView, name='book_detail'),
	url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my_borrowed'),
]