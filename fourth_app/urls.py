from django.urls import path     
from . import views
urlpatterns = [ path('', views.index), 
               path('register', views.register),
               path('login', views.login),
               path('wall', views.wall),
               path('mes', views.wall,name='message'),
               path('com', views.comment,name='comment'),   
                   
               
                 ]