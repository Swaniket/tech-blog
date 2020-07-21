from django.contrib import admin
from django.urls import path, include
from blogApp import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
     # API to post a comment
    path('postComment/', views.postComment, name ='postComment'),
    # <str:slug> can put the query into views
    path('<str:slug>', views.blogPost, name='blogPost'),

   
    
]