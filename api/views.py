from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from api.serializers import RegisterUserSerializer, LoginSerializer, ChatSerializer, MessagesSerializer, UserSerializer, ChatCreateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.token_auth import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User

from message_app.models import Chat, Contact

class UserRegistration(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=201)
        return Response({'message': 'Something went wrong while creating account'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            token = JWTAuthentication.generate_token(payload=serializer.data)
            return Response({
                "message": "Login successful",
                "token": token,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChats(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        serializer = ChatCreateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        contact = Contact.objects.filter(user=request.user).first()
        chats = contact.receiver.all()
        chats_2 = contact.sender.all()
        total_chats = chats | chats_2
        total_chats = total_chats.order_by('-updated')
        serializer = ChatSerializer(total_chats, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatMessages(ListAPIView):
    permission_classes = [IsAuthenticated,]


    def list(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=request.query_params['chat_id'])
        except (Chat.DoesNotExist, ValueError):
            return Response({'error':'CHAT_DOES_NOT_EXIST'}, status=status.HTTP_404_NOT_FOUND)
        qs = chat.messages.order_by('timestamp')
        serializer = MessagesSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class to return a list of users to be added as a chat option
class ChatUsers(ListAPIView):
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        sugg = request.query_params['suggestion']
        if len(sugg) > 0:
            qs = User.objects.filter(username__contains=sugg).exclude(username=request.user.username)
        else:
            qs = User.objects.all().exclude(username=request.user.username)
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_last_100_messages(chat_id, request=None):
    try:
        chat = Chat.objects.get(id=chat_id)
    except (Chat.DoesNotExist, ValueError):
        return {'failed': True, 'message':'Chat Does Not Exist'}
    return {'failed': False,'messages':chat.messages.order_by('-timestamp')[:100]}