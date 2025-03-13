from rest_framework import serializers
from rolesserializers import Role

class RoleSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField(max_length=255, unique=True, primary_key=True, editable=False) 
        name = serializers.CharField(max_length=255, unique=True)
        is_active = serializers.BooleanField(default=True)
        creation_date = serializers.DateTimeField(default=True)
        updation_date = serializers.DateTimeField(default=True)

 
class Meta:
         model = Role
         exclude = ['id','creation_data','updation_date']
         fields = ['id', 'name', 'is_active', 'creation_date', 'updation_date']
         read_only_field = ['creation_data','updation_date']


def validate_role(self,data):
        return data
                 
