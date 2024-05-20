from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    #Added section
    birthDate = models.DateTimeField(default=datetime.fromisoformat("2000-01-01"))
    favoriteMeat =models.CharField(max_length=100, default="unspecified")
    favoriteCooking =models.CharField(max_length=100, default="unspecified")
    favoriteRegion =models.CharField(max_length=100, default="unspecified")
    
    @property
    def get_photo_url(self):
        if self.profileimg and hasattr(self.profileimg, 'url'):
            return self.profileimg.url
        else:
            return "KeftaClubKeftaClub\media\blank-profile-picture.png"
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    #Added section
    Meat =models.CharField(max_length=100, default="unspecified")
    Cooking =models.CharField(max_length=100, default="unspecified")
    Region =models.CharField(max_length=100, default="unspecified")
    location = models.CharField(max_length=100, default="unknown")


    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    

class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
	date = models.DateTimeField(default=datetime.now)
	is_read = models.BooleanField(default=False)

class Room(models.Model):
    name = models.CharField(max_length=2000)

class Message(models.Model):
    value = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now , blank = True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    
