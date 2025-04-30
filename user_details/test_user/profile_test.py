import pytest
from user_details.models import Profile, User
from rest_framework.test import APIClient
from django.urls import reverse
import json
import pytest
import requests
import unittest
from unittest import mock
from django.utils import timezone
from django.contrib.auth.hashers import make_password

@mock.patch('user_details.views.ProfileSerializer')
class TestCreateProfileViews(unittest.TestCase):
    data = {
        "app": "StandaloneApp",
        "profile": "Admin",
        "user_id": "3"
    }
    def setup(self):
        self.client = APIClient()
        self.url = reverse('create_profile')
        self.profile_data = self.data


    def postreq(self):
        with mock.patch('user_details.views.requests.post'):
                # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
          return self.client.post(self.url, data=json.dumps(self.profile_data), content_type="application/json")
        

    


@mock.patch('user_details.views.ProfileSerializer')
class TestUpdateProfileViews(unittest.TestCase):
    data = {
        "app": "FoodApp",
        "profile": "Developer",
        "user_id": "3"
    }
    def setup(self):
        self.client = APIClient()
        self.url = reverse('update_profile',kwargs={'profile_id': self.data['id']})
        self.profile_data = self.data


    def putreq(self):
        with mock.patch('user_details.views.requests.put'):
                # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
          return self.client.put(self.url, data=json.dumps(self.profile_data), content_type="application/json")
        


# @mock.patch('user_details.views.ProfileSerializer')
# class TestDeleteProfileViews(unittest.TestCase):
#     data = {
#         "app": "MyNewApp",
#         "profile": "Admin",
#         "user_id": "3"
#     }
#     def setup(self):
#         self.client = APIClient()
#         self.url = reverse('delete_profile',kwargs={'profile_id': self.data['id']}) 

#     def deletereq(self):
#         with mock.patch('user_details.views.requests.delete'):
#                 # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
#           return self.client.delete(self.url)           




