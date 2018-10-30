from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name ="index"),
    url(r'^allquotes$', views.allquotes, name ="allquotes"),
    url(r'^create/$', views.create, name='create'),
    url(r'^login/$', views.login, name="login"),
    url(r'^addquote$', views.addquote, name='addquote'),
    url(r'^likes$', views.likes, name='likes'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'^(?P<id>\d+)/userquotes/$', views.userquotes, name ="userquotes"),
    url(r'^(?P<id>\d+)/myaccount/$', views.myaccount, name ="myaccount"),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^logout/$', views.logout, name='logout'),
]