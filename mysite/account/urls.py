from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^login/$', views.signin, name="login"),
    url(r'^register/$', views.signup, name="register"),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w+]*\w+)/$', views.active_user, name="activate"),
    url(r'^password-change/$', auth_views.password_change,{"post_change_redirect":"/account/password-change-done","template_name":"account/password_change_form.html"}, name="password_change"),
    url(r'^password-change-done/$', views.password_change_done, name="password_change_done"),
    
    url(r'^password-reset/$', auth_views.password_reset,{"template_name":"account/password_reset_form.html","email_template_name":"account/password_reset_email.html","post_reset_redirect":"/home"},name="password_reset"),
    url(r'password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,{"template_name":"account/password_reset_confirm.html","post_reset_redirect":"/home"}, name="password_reset_confirm"),
    url(r'^logout/$', auth_views.logout,{"template_name":"home.html"}, name="user_logout"),
    
    url(r'^my-info/$', views.my_info, name="my_info"),
    url(r'^my-info-edit/$', views.my_info_edit, name="my_info_edit"),
    url(r'^my-image/$', views.my_image, name="my_image"),

    url(r'^blog_remove/$', views.blog_remove, name="blog_remove"),
    url(r'^my-blog-list/(?P<column_id>\d+)/$', views.my_blog_list, name="my_blog_list"),
  
]

