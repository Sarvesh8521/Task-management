from django.shortcuts import render
from models import User
from serializers import Userserializer

def user_name(request):
    emp = User.objects.get()
