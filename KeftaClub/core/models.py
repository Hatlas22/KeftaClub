from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone

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
    favoriteSpicyness =models.CharField(max_length=100, default="0")
    favoriteCooking =models.CharField(max_length=100, default="burnt")
    favoriteOrigin =models.CharField(max_length=100, default="Leftovers")
    
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
    Spicyness =models.CharField(max_length=100, default="0")
    Cooking =models.CharField(max_length=100,  default="burnt")
    Origin =models.CharField(max_length=100,  default="Leftovers")
    location = models.CharField(max_length=100, default="unknown")


    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, default='unknown')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)
    

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
    
