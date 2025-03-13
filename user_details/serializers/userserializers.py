from rest_framework import serializers
from user_details import User

class UserSerializer(serializers.Modelserializer):
       id = serializers.BigAutoField(unique=True, primary_key=True)
       user_id = serializers.BigAutoField(primary_key=True, editable=False, unique=True)
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
            return value
       
       def validate_email_id(self,value):
            #icontai@gmail.com
            
            return value
       
       def validate_password(self,value):
            if len(value) < 8:
             raise ValueError("Password must be at least 8 characters long.")
            
            return value
       

       def validate(self,data):
           return data

