from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core import views
import uuid

class UrlsTest(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_settings_url_resolves(self):
        url = reverse('settings')
        self.assertEqual(resolve(url).func, views.settings)

    def test_upload_url_resolves(self):
        url = reverse('upload')
        self.assertEqual(resolve(url).func, views.upload)

    def test_follow_url_resolves(self):
        url = reverse('follow')
        self.assertEqual(resolve(url).func, views.follow)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, views.search)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['testuser'])
        self.assertEqual(resolve(url).func, views.profile)

    def test_like_post_url_resolves(self):
        url = reverse('like-post')
        self.assertEqual(resolve(url).func, views.like_post)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, views.signup)

    def test_signin_url_resolves(self):
        url = reverse('signin')
        self.assertEqual(resolve(url).func, views.signin)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout)

    def test_post_detail_url_resolves(self):
        url = reverse('post_detail', args=['testpost'])
        self.assertEqual(resolve(url).func, views.post_detail)

    def test_delete_post_url_resolves(self):
        url = reverse('delete_post', args=[uuid.uuid4()])
        self.assertEqual(resolve(url).func, views.delete_post)

    def test_edit_comment_api_url_resolves(self):
        url = reverse('edit_comment_api', args=[1])
        self.assertEqual(resolve(url).func, views.edit_comment_api)

    def test_delete_comment_api_url_resolves(self):
        url = reverse('delete_comment_api', args=[1])
        self.assertEqual(resolve(url).func, views.delete_comment_api)

    def test_inbox_url_resolves(self):
        url = reverse('inbox')
        self.assertEqual(resolve(url).func.view_class, views.ListThreads)

    def test_create_thread_url_resolves(self):
        url = reverse('create-thread')
        self.assertEqual(resolve(url).func, views.create_thread_ajax)

    def test_thread_url_resolves(self):
        url = reverse('thread', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.ThreadView)

    def test_create_message_url_resolves(self):
        url = reverse('create-message', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.CreateMessage)

    def test_room_url_resolves(self):
        url = reverse('room', args=['testroom'])
        self.assertEqual(resolve(url).func, views.room)

    def test_send_url_resolves(self):
        url = reverse('send')
        self.assertEqual(resolve(url).func, views.send)

    def test_checkview_url_resolves(self):
        url = reverse('checkview')
        self.assertEqual(resolve(url).func, views.checkview)

    def test_getMessages_url_resolves(self):
        url = reverse('getMessages', args=['testroom'])
        self.assertEqual(resolve(url).func, views.getMessages)
