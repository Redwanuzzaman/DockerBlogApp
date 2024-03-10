# accounts/views.py
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Ensure that 'password' is present in the payload
        if 'password' not in request.data:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user with the provided data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use set_password to handle the password correctly
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Ensure that 'password' is present in the payload
        if 'password' in request.data:
            # Use set_password to handle the password correctly
            self.get_object().set_password(request.data['password'])

        # Update the user with the provided data
        return super().update(request, *args, **kwargs)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
