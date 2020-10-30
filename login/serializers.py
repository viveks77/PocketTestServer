from .models import User, Standard
from django.contrib.auth import authenticate
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name","email","password","mobile_no","location","class_no")
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data["email"],validated_data["password"],validated_data["mobile_no"])
        user.name = validated_data["name"]
        user.location = validated_data["location"]
        user.class_no = validated_data["class_no"]
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            return user
        raise serializers.ValidationError("Incorrect credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "mobile_no", "location", "is_student", "class_no")

    

class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "location"]

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = "__all__"