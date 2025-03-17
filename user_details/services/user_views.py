from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from user_details.models import User  
from user_details.serializers import UserSerializer  

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

   
    def create_user(self):
        serializer = self.get_serializer()

        
        if serializer.is_valid():
           
            user = serializer.save()

           
            return Response(serializer.data)
        else:
            
            return Response(serializer.errors)

    

    def update_user(self, pk=None):
        try:
            user = User.objects.get(pk=pk) 
        except User.DoesNotExist:
            return Response({'error': 'User not found'})
        serializer = self.get_serializer()

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    
    def delete_user(self, pk=None):
        try:
            user = User.objects.get(pk=pk)  
        except User.DoesNotExist:
            return Response({'error': 'User not found'})

        
        user.delete()
        return Response({'message': 'User deleted'})

    

    
    def list_users(self):
        
        users = User.objects.all()

    
        serializer = self.get_serializer()
        return Response(serializer.data)