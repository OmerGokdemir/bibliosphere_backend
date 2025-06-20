from datetime import datetime
from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already exist.")]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('firstName','lastName','address','phone','birthDate','email','password',"resetPasswordCode")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        token = super().get_token(user)


        token.set_exp(lifetime=datetime.timedelta(days=30))

        return token

class CustomLoginSerializer(CustomTokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def get_token(self, user):
        token = super().get_token(user)

        # Token süresini burada ayarlayabilirsiniz
        # Örneğin, 30 gün olarak ayarlamak için:
        token.set_exp(lifetime=datetime.timedelta(days=30))

        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')
        

class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
        "password", "resetPasswordCode","newPassword")

    newPassword = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','firstName','lastName','address','phone','birthDate','email','password',"score","is_superuser","score","is_staff")

    

class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id',"score",'firstName','lastName','address',"resetPasswordCode",'phone','birthDate','email','password',"is_superuser","is_staff")

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])

        user.save()
        return user
    


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id','firstName',"createDate",'lastName','address','phone','birthDate','email','password',"is_superuser","is_staff","score","password","resetPasswordCode")

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)