import pytest
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient
from user_details.models import User
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient
import json
from user_details.serializers.userserializers import UserSerializer
import unittest
import requests
from unittest import mock
import pytest


@mock.patch('user_details.userviews.user_views.requests')   
class TestUserViews(unittest.TestCase):
    data={
        "user_name": "Laddo",
        "email_id": "Laddo@example.com",
        "password": "secure_password"
    }
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_user')
        self.user_data = self.data

    

    def postreq(self):
        with mock.patch('user_details.userviews.user_views.requests.post'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.post(self.url, data=json.dumps(self.user_data), content_type="application/json")
        
    @pytest.mark.django_db
    def test_create_user(self):
        response = self.postreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
           
        



@mock.patch('user_details.userviews.user_views.requests')
class TestUpdateUserViews(unittest.TestCase):
    data={
        'id': 1,
        "user_name": "quinton_k",                      
        "password": "Quinton@2025",                    
        "email_id": "quinton.k@example.com",           
        "first_name": "Quinton",
        "last_name": "Kapoor",     
    
}       
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('update_user',kwargs={'user_id': self.data['id']})
        self.user_data = self.data

    

    def putreq(self):
        with mock.patch('user_details.userviews.user_views.requests.put'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.put(self.url, data=json.dumps(self.user_data), content_type="application/json")

    @pytest.mark.django_db
    def test_update_user(self):
        response = self.putreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
            



@mock.patch('user_details.userviews.user_views.requests')
class TestDeleteUserViews(unittest.TestCase):
    data={
        'id': 1,
        "user_name": "quinton_k",                      
        "password": "Quinton@2025",                    
        "email_id": "quinton.k@example.com",           
        "first_name": "Quinton",
        "last_name": "Kapoor",     
    
}       
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('delete_user')
        self.user_data = self.data

    

    def deletereq(self):
        with mock.patch('user_details.userviews.user_views.requests.delete'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.delete(self.url,)


    @pytest.mark.django_db
    def test_delete_user(self):
        response = self.deletereq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)        


@mock.patch('user_details.userviews.user_views.requests')
class TestGetUserViews(unittest.TestCase): 
    data={
        'id': 1,
        "user_name": "quinton_k",                      
        "password": "Quinton@2025",                    
        "email_id": "quinton.k@example.com",           
        "first_name": "Quinton",
        "last_name": "Kapoor",
    }  
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get_user')

    def getreq(self):
        with mock.patch('user_details.userviews.user_views.requests.get'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.get(self.url)
        

    @pytest.mark.django_db
    def test_get_user(self):
        response = self.getreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

@mock.patch('user_details.userviews.user_views.requests')
class TestSearchUserViews(unittest.TestCase):
    data={
        'id': 1,
        "user_name": "quinton_k",                      
        "password": "Quinton@2025",                    
        "email_id": "quinton.k@example.com",           
        "first_name": "Quinton",
        "last_name": "Kapoor",
    }  
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search_user')

    def getreq(self):
        with mock.patch('user_details.userviews.user_views.requests.get'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.get(self.url) 
        

    @pytest.mark.django_db
    def test_search_user(self):
        response = self.getreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)    