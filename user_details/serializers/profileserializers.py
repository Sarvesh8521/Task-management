from rest_framework import serializers
from user_details.models import Profile, User  
from django.core.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    app = serializers.CharField(max_length=255)
    profile = serializers.CharField()  
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  
    class Meta:
        model = Profile
        exclude = [] 
        fields = ['id', 'app', 'profile', 'user']  
        read_only_fields = ['id']  

    def validate_user(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise ValidationError("User does not exist.")
        return value

    def validate_app(self, value):
        if not value:
            raise ValidationError("App field cannot be empty.")
        return value

    def validate_profile(self, value):
        if not value.strip():
            raise ValidationError("The profile cannot be empty.")
        return value
