from rest_framework import serializers
from user_details.models import RefreshToken
from user_details.models import Token
from user_details.models import User
from rest_framework.exceptions import ValidationError

class RefreshTokenSerializer(serializers.ModelSerializer):
         id = serializers.BigAutoField(unique=True, primary_key=True, editable=False) 
         user = serializers.ForeignKey(max_length=255, on_delete=serializers.CASCADE)
         refresh_token = serializers.TextField(unique=True)
         is_active = serializers.BooleanField(default=True)
         counter = serializers.IntegerField(default=0)
         token = serializers.ForeignKey(on_delete=serializers.CASCADE)
         expires_at = serializers.DateTimeField(LocalTimezone=True)
         creation_date = serializers.DateTimeField(LocalTimezone=True)
         updation_date = serializers.DateTimeField(LocalTimezone=True)




class Meta:
        model = RefreshToken
        read_only_feild = ['creation_date', 'expires_at','updation_date']
        exclude = ['id','user','token']
        fields = ['id', 'user', 'refresh_token', 'is_active', 'counter', 'token', 'expires_at', 'creation_date', 'updation_date']



def validate_token(self, value):
        if not Token.exists():
            raise ValidationError(f"The token does not exist.")
        return value



def validate_refresh_tokens(self,data):
        if RefreshToken.exists():
            raise ValidationError("The refresh token must be unique")
        
        if not data.get('refresh_token'):
             raise ValidationError("Refresh token cannot be null")
        return data


def validate_counter(self, value):
        if value < 0:
            raise ValidationError("The counter must be a non-negative integer.")
        return value


def validate_is_active(self, value):
        if not value:
            raise ValidationError("The is_active field cannot be null.")
        return value


def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value
