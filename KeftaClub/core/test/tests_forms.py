from django.test import TestCase
from core.forms import *
from core.models import Comment, MessageModel
from django.contrib.auth.models import User
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class CommentFormTest(TestCase):

    def test_comment_form_valid_data(self):
        form = CommentForm(data={'body': 'This is a test comment'})
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('body', form.errors)

class ThreadFormTest(TestCase):

    def test_thread_form_valid_data(self):
        form = ThreadForm(data={'username': 'testuser'})
        self.assertTrue(form.is_valid())

    def test_thread_form_no_data(self):
        form = ThreadForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('username', form.errors)

class MessageFormTest(TestCase):

    def test_message_form_valid_data(self):
        form = MessageForm(data={'body': 'This is a test message'})
        self.assertTrue(form.is_valid())

    def test_message_form_no_data(self):
        form = MessageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('body', form.errors)
    
    
    def create_test_image(self):
        # Create a simple image using Pillow
        image = Image.new('RGB', (10, 10), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile("image.jpg", image_file.read(), content_type="image/jpeg")

    def test_message_form_valid_data_with_image(self):
        image = self.create_test_image()
        form = MessageForm(data={'body': 'This is a test message'}, files={'image': image})
        self.assertTrue(form.is_valid(), msg=f"Errors: {form.errors}")

    def test_message_form_only_image(self):
        image = self.create_test_image()
        form = MessageForm(files={'image': image})
        self.assertFalse(form.is_valid(), msg="The form should not be valid without the body.")
        self.assertEqual(len(form.errors), 1, msg=f"Expected one error, got: {form.errors}")
        self.assertIn('body', form.errors, msg=f"Errors: {form.errors}")
