from .models import User, Standard
from django.shortcuts import render
from .serializers import UserSerializer, RegisterSerializer,  LoginSerializer, ResetPasswordSerializer, UserUpdateSerializer, ClassSerializer
from rest_framework.response  import Response
from rest_framework import generics
from knox.auth import AuthToken
from rest_framework.generics import GenericAPIView,RetrieveAPIView, UpdateAPIView
from rest_framework import permissions, status

#Login Api
class LoginAPI(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            'user': UserSerializer(user).data,
            'token':AuthToken.objects.create(user)[1]
        })

#Register Api 
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user':UserSerializer(user).data
        })


#Get user information
class UserAPI(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user


#Reset user password
class ResetPasswordAPI(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            #checks if old password is correct
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old password" : "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({
                'status':"success"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Update user information
class UserUpdateAPI(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.name = serializer.data.get('name')
            user.mobile_no = serializer.data.get('mobile_no')
            user.location = serializer.data.get('location')
            user.class_n0 = serializer.data.get('class_no')
            user.save()
            return Response({
                "user":UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassListAPI(generics.ListAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):
        return Standard.objects.all()