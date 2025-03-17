from rest_framework import serializers
from scopesserializers import Scopes
from rest_framework import ValidationError

class ScopeSerializer(serializers.Modelserializers):
        id =serializers.BigAutoField( primary_key=True) 
        name =serializers.ForeignKey(max_length=255, unique=True)
        is_active =serializers.BooleanField(default=True)
        updation_date =serializers.DateTimeField(LocalTimezone=True)



class Meta:
        model = Scopes
        exclude = ['id']
        read_only_feild = ['updation_date']
        fields = ['id', 'role', 'is_active', 'updation_date']


def validate_scope(self,data):
        if Scopes.exists():
            raise ValidationError(f"A scope with the name  exists")
        return data

def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise ValidationError("True/False")
        return value

def validate_name(self, value):
        if Scopes.exists():
            raise ValidationError(f"scope with the name  already exists.")
        return value