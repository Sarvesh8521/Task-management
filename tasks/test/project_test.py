import json
from rest_framework.test import APIClient
from tasks.models import Task, Project
from tasks.serializers.taskserializers import TaskSerializer
from user_details.models import User
from rest_framework import status
import unittest
import pytest
import requests
from unittest import mock
from django.urls import reverse


@mock.patch('tasks.tasksviews.ProjectSerializer')
class TestProjectViews(unittest.TestCase):
    data = {
         "id": 10,
         "name": "Task Management",
         "super_user": 2,
         "sub_user": 1,
         "user": 2,
         "status": "planned",
         "release_version": "v0.2",
         "sprint": 3
       
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_project')
        self.project_data = self.data

    def postreq(self):
        with mock.patch('tasks.tasksviews.requests.post'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.post(self.url, data=json.dumps(self.data), content_type="application/json")
        


    @pytest.mark.django_db
    def test_create_project(self):
        response = self.postreq()    
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
        
        

@mock.patch('tasks.tasksviews.ProjectSerializer')
class TestUpdateProjectViews(unittest.TestCase):
    data = {
        
         "id": 10,
         "name": "Project Kuhoo",
         "super_user": 2,
         "sub_user": 1,
         "user": 2,
         "status": "planned",
         "release_version": "v0.1",
         "sprint": 2
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('update_project',kwargs={'project_id': self.data['id']})
        self.project_data = self.data

    def putreq(self):
        with mock.patch('tasks.tasksviews.requests.put'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.put(self.url, data=json.dumps(self.data), content_type="application/json")
        


    @pytest.mark.django_db
    def test_update_project(self):    
        response = self.putreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        




@mock.patch('tasks.views.ProjectSerializer')
class TestDeleteProjectViews(unittest.TestCase):
    data = {
        "name": "test project",
        "description": "test description",
        "users": 1,
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('delete_project')

    def test_delete_project(self):
        with mock.patch('tasks.views.requests.delete'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.delete(self.url)
        

@mock.patch('tasks.views.ProjectSerializer')
class TestGetProjectViews(unittest.TestCase):
    data = {
        "name": "test project",
        "description": "test description",
        "users": 1,
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get_project')

    def test_get_project(self):
        with mock.patch('tasks.views.requests.get'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.get(self.url) 