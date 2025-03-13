from rest_framework import serializers
from organizationserializers import Organization

class OrganizationSerializer(serializers.ModelSerializer):
        id = serializers.BigAutoField( unique=True, primary_key=True)
        name = serializers.ForeignKey(max_length=255, unique=True,)
        super_user = serializers.ForeignKey(on_delete=serializers.CASCADE,)
        sub_user = serializers.ForeignKey()
        creation_date = serializers.DateTimeField(LocalTimezone=True)
        updation_date = serializers.DateTimeField(LocalTimezone=True)
        is_active = serializers.BooleanField(default=True)


class Meta:

        model = Organization
        read_only_fields = ['creation_date', 'updation_date', 'is_active']
        exclude = ['id', 'name','sub_user',]
        fields = ['id', 'name', 'super_user', 'sub_user', 'creation_date', 'updation_date', 'is_active']


def validate_Organization(self,data):
        return data