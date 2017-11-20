from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name ='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView, name='project_detail'),
    url(r'^chapter/(?P<pk>\d+)$', views.ChapterDetailView, name='chapter_detail'),
    url(r'^articles/$', views.ArticleListView.as_view(), name='articles'),
    url(r'^article/(?P<pk>\d+)$', views.ArticleDetailView, name='article_detail'),
    url(r'^projects/create/$', views.ProjectCreationView, name='project_creation'),
    url(r'^project/createchapter/$', views.ChapterCreationView, name='chapter_creation'),
    url(r'^chapter/edit/(?P<pk>([^$]+))$', views.ChapterEditView, name='chapter_edit'),
    url(r'^searchpage/search', views.search, name='search'),  # search results. No$ because it will continue with stuff
    url(r'^searchpage/$', views.search_page, name='searchpage'), #search page
    url(r'^editpage/(?P<pk>\d+)$', views.ArborescenceEditView, name='edit_repository'),
    url(r'^editrepo/(?P<pk>\d+)$', views.PersonalArborescenceEditView, name='edit_personal_repository'),
]
