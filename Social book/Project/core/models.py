from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
import uuid #helps us generate unique ID
from datetime import datetime #the data that the post was uploaded

User = get_user_model()
#a table in the database, we will migrate it in the database
class Profile(models.Model):  #calls get_user_model() the foreign key is for following another user
    user = models.ForeignKey(User, on_delete=models.CASCADE) #rows in the table
    id_user = models.IntegerField()
    bio = models.TextField(blank=True) #the folder in media folder, every media stored there will be stored in that folder
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)#primary_key=True to replace the default ID of 0,1,2 with something unique
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default = datetime.now)
    no_of_likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length = 500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username #not user.username because this is a foreign key so its not an object being passed in, only the user is being passsed

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user