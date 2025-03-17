from rest_framework import serializers
from tokensserializers import Token
from user_details.models import User
from user_details.models import RefreshToken
from rest_framework.exceptions import ValidationError

class TokenSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField(primary_key=True) 
        user = serializers.ForeignKey(max_length=255, on_delete=serializers.CASCADE)
        access_token = serializers.TextField(unique=True)
        token_type = serializers.CharField(max_length=10)
        refresh_token = serializers.ForeignKey(on_delete=serializers.CASCADE)

class Meta:
        model = Token
        read_only_feilds = ['access_token','token_type','refresh_tokens']
        exclude = ['id','user']
        fields = ['id', 'user', 'access_token', 'token_type', 'refresh_token']


def validate_access_token(self, value):
       
        if Token.objects.filter(access_token=value).exists():
            raise ValidationError("Access token must be unique.")
        return value

def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value

#def validate_token_type(self, value):
 #       allowed_token_types = ["Bearer"]
  #      if value not in allowed_token_types:
   #         raise ValidationError(f"Token type must be one of ")
    #    return value

def validate_refresh_token(self, value):
        if not value:
            raise ValidationError("Refresh token cannot be null.")
        
        
        #if not RefreshToken.exists():
         #   raise ValidationError("Refresh token does not exist.")
        return value


def validate_tokens(self,data):
        if Token.exists():
            raise ValidationError("This user already has this access token assigned.")
        return data