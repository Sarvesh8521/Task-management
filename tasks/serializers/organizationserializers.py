from rest_framework import serializers
from organizationserializers import Organization
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class OrganizationSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField( unique=True, primary_key=True)
        user = serializers.ForeignKey(max_length=255, on_delete=serializers.CASCADE,)
        name = serializers.ForeignKey(max_length=255, unique=True)
        super_user = serializers.CharField(user, max_length=255, unique=True)
        sub_user = serializers.CharField(user ,max_length=255, unique=True)
        creation_date = serializers.DateTimeField(LocalTimezone=True)
        updation_date = serializers.DateTimeField(LocalTimezone=True)
        is_active = serializers.BooleanField(default=True)
        sprint = serializers.CharField(max_length=100, null=True, blank=True, default=1)


class Meta:     

        model = Organization
        read_only_fields = ['creation_date', 'updation_date', 'is_active']
        exclude = ['id', 'name','sub_user',]
        fields = ['id', 'name', 'super_user', 'sub_user', 'creation_date', 'updation_date', 'is_active']


def validate_organization(self,data):
        if data.get('super_user') == data.get('sub_user'):
            raise ValidationError("you've assigned the same person as both")
       # validate_organization = OrganizationSerializer(data=data)
        return data
    


def validate_super_user(self, value):

        if value == self.data.get('sub_user'):
            raise ValidationError("Please choose a different sub user.")
        return value

def validate_sub_user(self, value):
       
        if value == self.data.get('super_user'):
            raise ValidationError(" Please choose a different super user.")
        return value

def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value






#def create_organization(self, pk=None):
    #serializer = self.get_serializer()
    #if serializer.is_valid():
     #   organization = serializer.save()
      #  return Response(serializer.data)
    #else:
     #   return Response(serializer.errors)


#def validate_name(self, value):
        
 #       if Organization(name=value).exists():
  #          raise ValidationError(" Please choose a different name.")
   #     return value