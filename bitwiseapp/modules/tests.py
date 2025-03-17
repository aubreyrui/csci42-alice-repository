from django.test import TestCase
from django.contrib.auth.models import User

from .models import ModuleCategory, Module, Comment
from accounts.models import Profile 


class ModuleCategoryTest(TestCase): 
    @classmethod 
    def setUpTestData(cls):
        return 0

class ModuleTest(TestCase): 
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='test_user', password='12345@BbBb')
        Profile.objects.create(user=user1, display_name='Bob', email='name@test.com')
        