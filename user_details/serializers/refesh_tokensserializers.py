from rest_framework import serializers
from user_details.models import RefreshToken

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


def validate_refresh_tokens(self,data):
        return data