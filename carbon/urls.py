from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home1, name="home1"),
    path('home1', views.home1, name="home1"),




    path('home2', views.home2, name="home2"),
    path('carbons', views.carbons, name="carbons"),
    path('carbonresult', views.carbonresult, name="carbonresult"),
    path('logins', views.logins, name="logins"),
    path('register',views.register,name='register'),
    path('forgetpassword',views.forgetpassword,name='forgetpassword'),
    path('articles',views.articles,name='articles'),
    path('searchhome', views.searchhome,name='searchhome'),
    path('searchresults',views.searchresults,name='searchresults'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout,name='logout'),

    path('SAPLING/redir',views.redir,name='redir'),

    path('weather', views.weather, name='weather'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),

    path('community',views.community, name='community'),
    path('saplinghome', views.saplinghome, name='saplinghome'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]
