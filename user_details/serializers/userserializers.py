from rest_framework import serializers
from user_details.models import User

from rest_framework.exceptions import ValidationError
import re

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    user_id = serializers.UUIDField(read_only=True)  
    user_name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email_id = serializers.EmailField(max_length=124)
    password = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(default=True)
    creation_date = serializers.DateTimeField()
    updation_date = serializers.DateTimeField()

    class Meta:
        model = User
        exclude = []  
        read_only_fields = ['user_id']
        fields = ['id','user_id', 'user_name', 'first_name', 'last_name', 'email_id', 'password', 'is_active', 'creation_date', 'updation_date']

    def validate_user_name(self, value): 
        if value is not None:
            if User.objects.filter(user_name=value).exists():
                raise serializers.ValidationError("Username already exists.")
        return value

    def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("(True/False)")
        return value

    def validate_email_id(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Please enter a valid email")
        return value

    def validate_password(self, value):
        validate_value_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$'
        if not re.match(validate_value_regex, value):
            raise serializers.ValidationError("Password must contain at least one uppercase, one lowercase, one number and one special character.")
        return value

    def validate_User(self, value):  
        if not User.objects.exists():  
            raise ValidationError("User does not exist.")
        return value
