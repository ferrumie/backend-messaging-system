from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.core.exceptions import ValidationError
from rest_framework import serializers  # type: ignore

from message_app.models import Chat, Contact, Messages

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            # if email exist raise error
            raise serializers.ValidationError("A user with this email allready exists")

        try:
            # Validate password
            password_validation.validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        return attrs

    def create(self, validate_data):
        user = User.objects.create_user(
            email=validate_data['email'], password=validate_data['password'], username=validate_data.get('username', "")
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
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        return {
            "email": user.email,
            "id": user.id,
            "username": user.username,
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessagesSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ['sender_username', 'content', 'timestamp']

    def get_sender_username(self, message):
        return message.contact.user.username


class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message_sent = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'user', 'last_message_sent']
        depth = 2

    def get_last_message_sent(self, chat):
        message = chat.messages.last()
        serializer = MessagesSerializer(message)
        return serializer.data

    def get_user(self, chat):
        try:
            user = self.context['request'].user
        except KeyError:
            user = self.context['user']

        # check if the logged in user is the sender or the receiver
        user_2 = chat.receiver.user if chat.sender.user == user else chat.sender.user

        serializer = UserSerializer(user_2)
        return serializer.data


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class ChatCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = ['user_id']

    def create(self, validated_data):
        req_user = self.context['request'].user
        user_id = validated_data['user_id']
        user = User.objects.get(id=user_id)
        contact, created = Contact.objects.get_or_create(user=user)
        req_contact, created = Contact.objects.get_or_create(user=req_user)

        chat = Chat.objects.get(user_one=req_contact, user_two=contact)

        return ChatSerializer(chat, context={'user': req_user}).data
