
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from asgiref.testing import ApplicationCommunicator
import pytest

from messaging_system.asgi import application 
from asgiref.sync import sync_to_async

User = get_user_model()

@pytest.mark.asyncio
class TestChatConsumer:

    async def generate_jwt_token(self, user):
        payload = {
            'email': user.email,
            'password': user.password,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    async def test_authentication(self, db):
        # Create a test user
        user = await sync_to_async(User.objects.create_user)(email='test@gmail.com', username='testuser', password='testpassword')

        # Generate JWT token
        token = await self.generate_jwt_token(user)
        
        # Connect to the WebSocket with JWT token as query parameter
        communicator = WebsocketCommunicator(
            application, f"/ws/chat/blah?token={token}"
        )
        
        connected, _ = await communicator.connect()
        breakpoint()
        assert connected, "WebSocket connection failed."

        # Send a test message
        await communicator.send_json_to({"message": "Hello, world!"})
        
        # Receive response from the WebSocket
        response = await communicator.receive_json_from()
        assert response["message"] == "Hello, world!", "Message response mismatch."

        # Disconnect the WebSocket
        await communicator.disconnect()

    async def test_invalid_token(self, db):
        # Try to connect with an invalid token
        communicator = WebsocketCommunicator(
            application, "/ws/chat/?token=invalidtoken"
        )
        
        connected, _ = await communicator.connect()
        assert not connected, "Connection should not succeed with an invalid token."

        # Disconnect if connected (for safety in case of unexpected behavior)
        await communicator.disconnect()

    
    async def test_message_broadcast(self, db):
    # Create two test users and their JWT tokens
        user1 = await sync_to_async(User.objects.create_user)(email='test1@gmail.com', username='user1', password='password123')
        user2 = await sync_to_async(User.objects.create_user)(email='test2@gmail.com', username='user2', password='password123')
        token1 = await self.generate_jwt_token(user1)
        token2 = await self.generate_jwt_token(user2)
        
        # Connect both users to the same room
        communicator1 = WebsocketCommunicator(
            application, f"/ws/chat/room1/?token={token1}"
        )
        communicator2 = WebsocketCommunicator(
            application, f"/ws/chat/room1/?token={token2}"
        )
        
        connected1, _ = await communicator1.connect()
        connected2, _ = await communicator2.connect()
        assert connected1, "User 1 failed to connect."
        assert connected2, "User 2 failed to connect."

        # User 1 sends a message
        await communicator1.send_json_to({"message": "Hello from user1"})
        
        # User 2 receives the message
        response = await communicator2.receive_json_from()
        assert response["message"] == "Hello from user1", "Broadcasting message failed."
        
        # Disconnect both users
        await communicator1.disconnect()
        await communicator2.disconnect()
