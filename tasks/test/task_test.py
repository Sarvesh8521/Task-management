import json
import pytest
from rest_framework.test import APIClient
from tasks.models import Task, Project
from django.urls import reverse
from tasks.serializers.taskserializers import TaskSerializer
from user_details.models import User
import unittest
import requests
from unittest import mock
from django.utils import timezone


@mock.patch('tasks.views.TaskSerializer')
class TestTaskViews(unittest.TestCase):
    data = {
        "name": "Public task",
        "description": "working on public task",
        "project": 2,
        "users": 2,
        "status": "todo"
    }

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_task')
        self.task_data = self.data


    def postreq(self):
        with mock.patch('tasks.views.requests.post'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.post(self.url, data=json.dumps(self.task_data), content_type="application/json")
        

         




@mock.patch('tasks.views.TaskSerializer')
class TestUpdateTaskViews(unittest.TestCase):
    data = {
        "id": 1,
        "name": "Public task",
        "description": "working on public task",
        "project": 2,
        "users": 2,
        "status": "todo"
    }

    def setUp(self):
        self.client = APIClient()
        self.task_id = 1
        self.url = reverse('update_task',kwargs={'task_id': self.task_id})
        self.task_data = self.data

    def putreq(self):
        with mock.patch('tasks.views.requests.put'):
            return self.client.put(self.url, data=json.dumps(self.task_data), content_type="application/json")           
        




# @mock.patch('tasks.views.TaskSerializer')
# class TestDeleteTaskViews(unittest.TestCase):
#     data = {
#         "name": "test task",
#         "description": "test description",
#         "project": 1,
#         "users": 1,
#         "status": "todo",
#         "start_date": "2023-01-01",
#         "end_date": "2023-01-02",
#         "sprint": "1",
#         "release_version": "1.0"
#     }
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('delete_task')

#     def test_delete_task(self):
#         with mock.patch('tasks.views.requests.delete'):
#             return self.client.delete(self.url)        


# @mock.patch('tasks.views.TaskSerializer')
# class TestGetTaskViews(unittest.TestCase):
#     data = {
#         "name": "test task",
#         "description": "test description",
#         "project": 1,
#         "users": 1,
#         "status": "todo",
#         "start_date": "2023-01-01",
#         "end_date": "2023-01-02",
#         "sprint": "1",
#         "release_version": "1.0"
#     }
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('get_task')

#     def test_get_task(self):
#         with mock.patch('tasks.views.requests.get'):
#             return self.client.get(self.url)

# @mock.patch('tasks.views.TaskSerializer')
# class TestAssignTaskViews(unittest.TestCase):
#     data = {
#         "name": "Public task",
#         "description": "working on public task",
#         "project": 2,
#         "users": 2,
#         "status": "todo"
#     }

#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('assign_task',kwargs={'task_id': self.task_id},kwargs={'user_id': self.user_id})
#         self.task_data = self.data

#     def test_assign_task(self):
#         with mock.patch('tasks.views.requests.post'):
#             return self.client.post(self.url, data=json.dumps(self.task_data), content_type="application/json")