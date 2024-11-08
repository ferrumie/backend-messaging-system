from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs["email"]).exists():
            # if email exist raise error
            raise serializers.ValidationError(
                "A user with this email allready exists")

        try:
            # Validate password
            password_validation.validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def create(self, validate_data):
        user = get_user_model().objects.create_user(
            email = validate_data['email'],
            password = validate_data['password'],
            first_name = validate_data.get('first_name', ""),
            last_name =validate_data.get('last_name', "")
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    id = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email is required for login")
        if password is None:
            raise serializers.ValidationError("A password is required for login")
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password"
                )
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        
        return{
            "email": user.email,
            "id": user.id,
            "username": user.username,
        }