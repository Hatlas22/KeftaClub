from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Profile, Post

class ViewTests(TestCase):

    def setUp(self):
        # Configuration initiale avant chaque test
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, id_user=1)
        self.client.login(username='testuser', password='12345')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_profile_view(self):
        response = self.client.get(reverse('profile', args=[self.profile.id_user]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_upload_view(self):
        with open('path/to/your/image.jpg', 'rb') as img:
            response = self.client.post(reverse('upload'), {'image': img, 'caption': 'Test caption'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful upload
        self.assertEqual(Post.objects.count(), 1)  # Verify that a post was created

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': '12345newuser',
            'password2': '12345newuser',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signin_view(self):
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful signin
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)
