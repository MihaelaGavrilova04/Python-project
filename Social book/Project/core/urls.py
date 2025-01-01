from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'), #this is so that the profile adds info about himself
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    #path('search/', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),#for the profile page(the link to get the profile page) to be able to get to the profilepage we need to go to profile/username(pk is a placeholder for username mai)
    path('like-post', views.like_post, name='like-post'), #the views cant have -
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]

