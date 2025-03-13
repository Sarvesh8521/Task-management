from rest_framework import serializers
from tokensserializers import Token

class TokenSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField(primary_key=True) 
        user = serializers.ForeignKey(on_delete=serializers.CASCADE)
        access_token = serializers.TextField(unique=True)
        token_type = serializers.CharField(max_length=10)
        refresh_token = serializers.ForeignKey(on_delete=serializers.CASCADE)

class Meta:
        model = Token
        read_only_feilds = ['access_token','token_type','refresh_tokens']
        exclude = ['id','user']
        fields = ['id', 'user', 'access_token', 'token_type', 'refresh_token']


def validate_tokens(self,data):
        return data