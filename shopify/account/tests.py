from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse

class ProfileTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    def test_str(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), f'Profile of {self.user.username}')

        
    