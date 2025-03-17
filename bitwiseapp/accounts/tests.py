from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile


class ProfileTest(TestCase): 
    @classmethod
    def setUpClass(cls):
        num_users = 12 

        for i in range(num_users): 
            userobj = User.objects.create_user(username=f'blaob{i}', password=f'{i}584719@HhHh')
            Profile.objects.create(user=userobj, display_name=f'Bob{i}', email=f'bob{i}@test.com')
    
    # TO-DO: test if genuine users can log-in to webpage 
    def login_accepts_genuine_user(self): 
        c = Client() 

        response = c.post("/login/")

    # TO-DO: test if users w/o accounts cannot log-in and are properly redirected

    # TO-DO: test account creation, if users are logged into the database 

    # TO-DO: check if email field works

    # TO-DO: check if password field works 