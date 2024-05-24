from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
import uuid

# Profile Model Test
class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            id_user=self.user.id,
            bio='This is a test bio',
            birthDate=datetime(2000, 1, 1),
            favoriteMeat='Beef',
            favoriteCooking='Grilling',
            favoriteRegion='North America'
        )
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.bio, 'This is a test bio')
        self.assertEqual(profile.birthDate, datetime(2000, 1, 1))
        self.assertEqual(profile.favoriteMeat, 'Beef')
        self.assertEqual(profile.favoriteCooking, 'Grilling')
        self.assertEqual(profile.favoriteRegion, 'North America')

# Post Model Test
class PostModelTest(TestCase):

    def test_post_creation(self):
        post = Post.objects.create(
            user='testuser',
            caption='This is a test post',
            Meat='Chicken',
            Cooking='Roasting',
            Region='Europe',
            location='Paris'
        )
        self.assertEqual(post.user, 'testuser')
        self.assertEqual(post.caption, 'This is a test post')
        self.assertEqual(post.Meat, 'Chicken')
        self.assertEqual(post.Cooking, 'Roasting')
        self.assertEqual(post.Region, 'Europe')
        self.assertEqual(post.location, 'Paris')
        self.assertIsInstance(post.id, uuid.UUID)

# LikePost Model Test
class LikePostModelTest(TestCase):

    def test_like_post_creation(self):
        like = LikePost.objects.create(post_id='1234', username='testuser')
        self.assertEqual(like.post_id, '1234')
        self.assertEqual(like.username, 'testuser')

# FollowersCount Model Test
class FollowersCountModelTest(TestCase):

    def test_followers_count_creation(self):
        follower_count = FollowersCount.objects.create(follower='testfollower', user='testuser')
        self.assertEqual(follower_count.follower, 'testfollower')
        self.assertEqual(follower_count.user, 'testuser')

# Comment Model Test
class CommentModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(user='testuser', caption='This is a test post')

    def test_comment_creation(self):
        comment = Comment.objects.create(post=self.post, body='This is a test comment', username='testuser')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.body, 'This is a test comment')
        self.assertEqual(comment.username, 'testuser')

# ThreadModel and MessageModel Test
class ThreadMessageModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.thread = ThreadModel.objects.create(user=self.user1, receiver=self.user2)

    def test_thread_creation(self):
        self.assertEqual(self.thread.user, self.user1)
        self.assertEqual(self.thread.receiver, self.user2)

    def test_message_creation(self):
        message = MessageModel.objects.create(
            thread=self.thread,
            sender_user=self.user1,
            receiver_user=self.user2,
            body='This is a test message'
        )
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.sender_user, self.user1)
        self.assertEqual(message.receiver_user, self.user2)
        self.assertEqual(message.body, 'This is a test message')

# Room and Message Model Test
class RoomMessageModelTest(TestCase):

    def test_room_creation(self):
        room = Room.objects.create(name='Test Room')
        self.assertEqual(room.name, 'Test Room')

    def test_message_creation(self):
        message = Message.objects.create(value='This is a test message', user='testuser', room='Test Room')
        self.assertEqual(message.value, 'This is a test message')
        self.assertEqual(message.user, 'testuser')
        self.assertEqual(message.room, 'Test Room')