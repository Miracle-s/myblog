from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^category/(?P<category_id>\d+)/$', views.category, name="category"),
    url(r'^column/(?P<column_id>\d+)/$', views.columnF, name="column"),

    url(r'^article-post/$', views.article_post, name="article_post"),
    url(r'^article-detail/(?P<article_id>\d+)/$', views.ArticleDetail.as_view(), name="article_detail"),
    url(r'^article-edit/(?P<article_id>\d+)/$', views.article_edit, name="article_edit"),
    
    url(r'^search/$', views.search, name='search'),

    url(r'^$', views.home, name='mysite_home'),
]
