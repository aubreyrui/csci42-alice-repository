from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileCreationForm


class ProfileTest(TestCase): 
    @classmethod
    def setUpClass(cls):
        num_users = 12 

        for i in range(num_users): 
            userobj = User.objects.create_user(username=f'blaob{i}', password=f'{i}584719@HhHh')
            Profile.objects.create(user=userobj, display_name=f'Bob{i}', email=f'bob{i}@test.com')
    
    # test if genuine users can log-in to webpage 
    def UNIT_login_accepts_genuine_user(self): 
        response = self.client.login(username='blaob1', password='1584719@HhHh')
        self.assertTrue(response)

    # test if users w/o accounts cannot log-in and are properly redirected
    def UNIT_login_rejects_fake_user(self): 
        response = self.client.login(username='iAMfake', password='F@k3P4s5w0r6')
        self.assertFalse(response)

    # test account creation, if users are logged into the database 
    def UNIT_can_create_valid_profile(self): 
        form_data = {'username': 'blaob13', 
                     'display_name': 'Bob13',
                     'email': 'bob13@test.com', 
                     'password1': '13584719@HhHh',
                     'password2': '13584719@HhHh'}
        form = ProfileCreationForm(data=form_data) 
        self.assertTrue(form.is_valid())

    # test invalid account creation, password1 diff. from password2
    def UNIT_cannot_create_invalid_profile(self): 
        form_data = {'username': 'blaob14', 
                     'display_name': 'Bob14',
                     'email': 'bob14@test.com', 
                     'password1': '14584719@HhHh',
                     'password2': '15584719@HhHh'}
        form = ProfileCreationForm(data=form_data) 
        self.assertFalse(form.is_valid())