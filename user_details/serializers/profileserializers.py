from rest_framework import serializers
from profile import Profile
from user_details.models import User
from django.core.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializers):
        id = serializers.BigAutoField(unique=True, primary_key=True) 
        app = serializers.CharField(max_length=255,)
        profile = serializers.TextField()
        user = serializers.ForeignKey(max_length=100)

class Meta:
        model = Profile
        exclude = ['app']
        fields = ['id', 'app', 'profile', 'user']
        read_only_feild = ['id']



def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value

def validate_app(self, value):
        
        if not value: 
            raise ValidationError("App field cannot be empty.")
        return value


def validate_profile(self,value, ):
             if not value.strip():  
                raise ValidationError("The profile cannot be empty")
             return value
