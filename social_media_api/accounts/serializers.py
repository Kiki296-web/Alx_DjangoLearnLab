from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

class RegisterSerializer(serializers.ModelSerializer):
    # explicitly use serializers.CharField() for password
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'bio', 'profile_picture']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # use get_user_model().objects.create_user
        user = get_user_model().objects.create_user(password=password, **validated_data)
        # explicitly create token with Token.objects.create
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            try:
                u = User.objects.get(email__iexact=email)
                user = authenticate(username=u.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs
