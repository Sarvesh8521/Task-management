from rest_framework import serializers
from user_rolesserializers import UserRole
from user_details.models import User
from rest_framework.exceptions import ValidationError

class UserRoleSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField(max_length=255, unique=True, primary_key=True) 
        user = serializers.ForeignKey(max_length=255, on_delete=serializers.CASCADE,)
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
     if UserRole.exists():
            raise serializers.ValidationError("This user already has role assigned.")
     return data


def validate_scope(self, value):
        if not value:
            raise serializers.ValidationError("null ")
        return value


def validate_role(self, value):
        if not value:
            raise serializers.ValidationError("Role cannot be null")
        return value


def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("(True/False)")
        return value

def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value


