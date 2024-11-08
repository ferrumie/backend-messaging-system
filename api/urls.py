from django.urls import path

from api.views import (ChatMessages, ChatUsers, UserChats, UserLogin,
                       UserRegistration)

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),
    path('chats/', UserChats.as_view(), name='user_chats'),
    path('add/', UserChats.as_view(), name='user_chats_add'),
    path('messages/', ChatMessages.as_view(), name='messages'),
    path('users/', ChatUsers.as_view(), name='users'),
]
