from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount
#importing the modules that we want to show in our admin profile
#when a user signes up, a profile module is authomatically going to be created for them
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)