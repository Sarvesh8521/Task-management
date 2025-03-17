from rest_framework import serializers
from organizationserializers import Organization

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
       # validate_organization = OrganizationSerializer(data=data)
        return data