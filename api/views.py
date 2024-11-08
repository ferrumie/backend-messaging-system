from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from api.serializers import RegisterUserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from accounts.token_auth import JWTAuthentication
from rest_framework import status

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
