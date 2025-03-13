from rest_framework import serializers
from profile import Profile

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


        def validate_profile(self,data):
             return data