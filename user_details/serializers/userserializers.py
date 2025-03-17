from rest_framework import serializers
from user_details import User 
from rest_framework.exceptions import ValidationError
import re

class UserSerializer(serializers.Modelserializer):
       id = serializers.BigAutoField( primary_key=True)
       user_id = serializers.BigAutoField(primary_key=True)
       user_name = serializers.CharField(max_length=50, unique=True)
       first_name = serializers.CharField(max_length=50)
       last_name = serializers.CharField(max_length=50)
       email_id = serializers.EmailField(unique=True,max_length=124)
       password = serializers.CharField(max_length=100)  
       is_active = serializers.BooleanField(default=True)
       creation_date = serializers.DateTimeField(LocalTimezone=True)
       updation_date = serializers.DateTimeField(LocalTimezone=True)



       class Meta:
         model = User
         exclude = ['id', 'user_id', 'user_name', 'first_name', 'last_name', 'email_id', 'password', 'is_active', 'creation_date', 'updation_date']
         read_only_feilds = ['user_id']
         fields = ['id', 'user_name', 'first_name', 'last_name', 'email', 'password', 'is_active', 'creation_date', 'updation_date']  


       def validate_username(self, value):
            if value is not None:
               if User.objects.filter(user_name=value).exists():
                   raise serializers.ValidationError("Username already exists.") 
                   
            return value
       

       def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("(True/False)")
        return value

       
       def validate_email_id(self,value):
            if "@" not in value:
              raise serializers.ValidationError("Please enter a valid email")
            #icontai@gmail.com
            
            return value
       
       def validate_password(self,value):
            validate_value_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$'
            if not re.match(validate_value_regex, value):
                  raise serializers.ValidationError("Password")
            return value
       
       def validate_user(self, value):
        if not User.exists():
            raise ValidationError(f"User does not exist.")
        return value


