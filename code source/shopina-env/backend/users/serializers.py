from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for public user information."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 
                 'avatar', 'role', 'plan', 'shop_name')
        read_only_fields = ('id', 'role')


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with all fields including address."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 
                 'avatar', 'phone_number', 'role', 'plan', 'shop_name', 'shop_slug',
                 'street_address', 'city', 'postal_code', 'country',
                 'is_verified', 'date_joined', 'last_password_change')
        read_only_fields = ('id', 'role', 'is_verified', 'date_joined', 'last_password_change')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'avatar',
                 'street_address', 'city', 'postal_code', 'country', 'shop_name', 'shop_slug', 'two_factor_enabled')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'role')
        extra_kwargs = {
            'role': {'default': 'CUSTOMER', 'required': False}
        }
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """Create user with validated data."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting password reset."""
    
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming password reset."""
    
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password while logged in."""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs


class TwoFactorVerifySerializer(serializers.Serializer):
    """Serializer for verifying an OTP."""
    otp = serializers.CharField(required=True, max_length=10)
    enable = serializers.BooleanField(required=False, default=False)


class TwoFactorStartSerializer(serializers.Serializer):
    """Empty serializer for starting 2FA (keeps interface consistent)."""
    pass



class EmailOrUsernameTokenObtainSerializer(TokenObtainPairSerializer):
    """Allow users to authenticate with email, username, or phone number."""
    
    identifier = serializers.CharField(required=True, write_only=False)
    password = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username field if it exists and replace with identifier
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        """Validate and authenticate user with flexible identifier."""
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        
        if not identifier or not password:
            raise serializers.ValidationError({
                'identifier': 'Both identifier and password are required.'
            })
        
        # Find user by email, username, or phone
        from django.db.models import Q
        from django.contrib.auth import authenticate
        
        try:
            user = User.objects.get(
                Q(email__iexact=identifier) | 
                Q(username__iexact=identifier) | 
                Q(phone_number=identifier)
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'identifier': 'No user found with this email, username, or phone.'
            })
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError({
                'identifier': 'Multiple accounts found. Please use your username.'
            })
        
        # Authenticate
        if not authenticate(username=user.username, password=password):
            raise serializers.ValidationError({
                'password': 'Invalid password.'
            })
        
        # Expose authenticated user to the view (for session login)
        self.user = user

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        return token

