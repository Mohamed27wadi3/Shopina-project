from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar', 'plan', 'shop_name')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmailOrUsernameTokenObtainSerializer(TokenObtainPairSerializer):
    """Allow users to authenticate with email OR username"""

    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        credentials = {
            'password': attrs.get('password')
        }
        username_or_email = attrs.get('username')
        # Try find by email
        try:
            user_obj = User.objects.get(email__iexact=username_or_email)
            credentials['username'] = user_obj.username
        except User.DoesNotExist:
            credentials['username'] = username_or_email

        return super().validate(credentials)
