from rest_framework import serializers
from user_rolesserializers import UserRole

class UserRoleSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField(max_length=255, unique=True, primary_key=True) 
        user = serializers.ForeignKey( on_delete=serializers.CASCADE)
        scope = serializers.ForeignKey()
        role = serializers.ForeignKey(on_delete=serializers.CASCADE)
        is_active = serializers.BooleanField(default=True)
        updation_date = serializers.DateTimeField(LocalTimezone=True)

        class Meta:
          model = UserRole
          read_only_Feilds = ['is_active','udation_date']
          exclude = ['id','scope',]
          fields = ['id', 'user', 'scope', 'role', 'is_active', 'updation_date']


def validate_user_role(self,data):
     return data