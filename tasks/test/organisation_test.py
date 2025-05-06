import json
import pytest
from rest_framework.test import APIClient
from tasks.models import Task, Project
from tasks.serializers.taskserializers import TaskSerializer
from user_details.models import User
from django.utils import timezone    
from django.urls import reverse
from rest_framework import status
import unittest
import requests
from unittest import mock


@mock.patch('tasks.tasksviews.organisation_views.OrganizationSerializer')
class TestCreateOrganisationViews(unittest.TestCase):
    data = {
        "name": "test org",
        "super_user": 1,
        "sub_user": 5
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_organization')
        self.org_data = self.data

    def postreq(self):
        with mock.patch('tasks.tasksviews.organisation_views.requests.post'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.post(self.url, data=json.dumps(self.org_data), content_type="application/json")
        
    @pytest.mark.django_db
    def test_create_organisation(self,mock_OrganizationSerializer):    
        response = self.postreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
        

@mock.patch('tasks.tasksviews.organisation_views.OrganizationSerializer')
class TestUpdateOrganisationViews(unittest.TestCase):
    data = {
        "name": "Reliance",
        "super_user": 1,
        "sub_user": 5
    }
    def setUp(self):
        self.client = APIClient()
        self.org_id = 1
        self.url = reverse('update_organization',kwargs={'org_id': self.org_id})
        self.org_data = self.data

    def putreq(self):
        with mock.patch('tasks.tasksviews.organisation_views.requests.put'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.put(self.url, data=json.dumps(self.org_data), content_type="application/json")
        

    @pytest.mark.django_db
    def test_update_organisation(self,mock_OrganizationSerializer):    
        response = self.putreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)








@mock.patch('tasks.tasksviews.organisation_views.OrganizationSerializer')
class TestDeleteOrganisationViews(unittest.TestCase):
    data = {
        "name": "test org",
         "super_user": 1,
         "sub_user": 5
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('delete_organisation')

    def test_delete_organisation(self):
        with mock.patch('tasks.tasksviews.organisation_views.requests.delete'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.delete(self.url)
        

@mock.patch('tasks.tasksviews.organisation_views.OrganizationSerializer')
class TestGetOrganisationViews(unittest.TestCase):
    data = {
        "org_id": 1,
        "name": "test org",
         "super_user": 1,
         "sub_user": 5
    }
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get_organisation')

    def test_get_organisation(self):
        with mock.patch('tasks.tasksviews.organisation_views.requests.get'):
            # requests_mock.post("https://external-service.com/endpoint", json={"key": "value"}, status_code=200)
            return self.client.get(self.url)
        
    @pytest.mark.django_db
    def test_get_organisation(self,mock_OrganizationSerializer):    
        response = self.postreq()
        self.assertEqual(response.status_code, status.HTTP_200_OK)    
