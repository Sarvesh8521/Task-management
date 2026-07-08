import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from user_details.models import User
from django.contrib.auth.models import User as AuthUser



class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    user_name = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email_id = serializers.EmailField(max_length=124)
    password = serializers.CharField(max_length=100, write_only=True)
    is_active = serializers.BooleanField(default=True)
    creation_date = serializers.DateTimeField(read_only=True)
    updation_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'user_id', 'user_name', 'first_name', 'last_name',
            'email_id', 'password', 'is_active', 'creation_date', 'updation_date',
        ]
        read_only_fields = ['id', 'user_id', 'creation_date', 'updation_date']

    def validate_user_name(self, value):
        """Allow same username on update, reject duplicates on create."""
        queryset = User.objects.filter(user_name=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email_id(self, value):
        """Allow same email on update, reject duplicates on create."""
        queryset = User.objects.filter(email_id=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters with uppercase, lowercase, number, and special character."
            )
        return value

    def create(self, validated_data):
        raw_password = validated_data['password']
        validated_data['password'] = make_password(raw_password)
        
        # Sync with Django Auth User for login
        auth_user, created = AuthUser.objects.get_or_create(
            username=validated_data['user_name'],
            defaults={
                'email': validated_data.get('email_id', ''),
                'first_name': validated_data.get('first_name', ''),
                'last_name': validated_data.get('last_name', '')
            }
        )
        auth_user.set_password(raw_password)
        auth_user.save()

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raw_password = validated_data.get('password')
        if raw_password:
            validated_data['password'] = make_password(raw_password)
            
            # Sync password update
            from django.contrib.auth.models import User as AuthUser
            try:
                auth_user = AuthUser.objects.get(username=instance.user_name)
                auth_user.set_password(raw_password)
                auth_user.save()
            except AuthUser.DoesNotExist:
                pass
                
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
