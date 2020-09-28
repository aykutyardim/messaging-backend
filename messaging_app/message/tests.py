from rest_framework.test import APITestCase, force_authenticate 
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from exceptions.models import ExceptionModel
from message.models import Message
import os

class Paths:
    MESSAGE = 'http://localhost:8000/api/message'
    SENT_MESSAGE = 'http://localhost:8000/api/message/sent'
    RECEIVED_MESSAGE = 'http://localhost:8000/api/message/received'
    CHAT_MESSAGE = 'http://localhost:8000/api/message/chat'
    DAILY_MESSAGE = 'http://localhost8000/api/message/daily'

class MessageTests(APITestCase):

    def setUp(self):
        """
        Create user object for Sent Messages tests
        """
        self.author = User.objects.create_user(username='author_user', password='123')
        self.target = User.objects.create_user(username='target_user', password='123')
        self.client.force_authenticate(user=self.author)

    def test_get_message(self):
        """
        Successful GET Messages Test
        """
        response = self.client.get(Paths.MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_message(self):
        """
        Successful POST Message Response Test
        """
        response = self.client.post(Paths.MESSAGE, {'target':'target_user','content':'contact me!'})        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        messages = Message.objects.filter()
        self.assertEqual(messages.count(), 1)
        
    def test_post_message_blank_data(self):
        """
        POST Message Test with Blank Data
        """
        response = self.client.post(Paths.MESSAGE, {'target' : ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        messages = Message.objects.all()
        self.assertEqual(messages.count(), 0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_post_message_invalid_data(self):
        """
        POST Message Test with Invalid Data
        """
        response = self.client.post(Paths.MESSAGE, {'target' : 'not_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.all()
        self.assertEqual(messages.count(), 0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_post_message_client_data(self):
        """
        POST Message Test with Client Data
        """
        response = self.client.post(Paths.MESSAGE, {'target' : 'author_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.all()
        self.assertEqual(messages.count(), 0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_post_message_missing_data(self):
        """
        POST Message Test with Missing Data 
        """
        response = self.client.post(Paths.MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.all()
        self.assertEqual(messages.count(), 0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)


class SentMessagesTests(APITestCase):
    
    def setUp(self):
        """
        Create user object for Sent Messages tests
        """
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_authenticate(user=self.user)

    def test_get_sent_messages(self):
        """
        Successful GET Sent Message List Test
        """
        response = self.client.get(Paths.SENT_MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class ReceivedMessagesTests(APITestCase):
    
    def setUp(self):
        """
        Create user object for Received Messages tests
        """
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_authenticate(user=self.user)

    def test_get_received_messages(self):
        """
        Successful GET Received Message List Test
        """
        response = self.client.get(Paths.RECEIVED_MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ChatTests(APITestCase):
    
    def setUp(self):
        """
        Create user objects for Chat Messages Tests
        """
        self.author = User.objects.create_user(username='author_user', password='123')
        self.target = User.objects.create_user(username='target_user', password='123')
        self.client.force_authenticate(user=self.author)

    def test_get_chat_messages(self):
        """
        Successful GET Chat Messages
        """
        response = self.client.get(Paths.CHAT_MESSAGE,{'target': 'target_user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chat_messages_invalid_data(self):
        """
        GET Chat Messages with Invalid Query String
        """
        response = self.client.get(Paths.CHAT_MESSAGE, {'target': 'not_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_get_chat_messages_missing_data(self):
        """
        GET Chat Messages with Missing Query String
        """
        response = self.client.get(Paths.CHAT_MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

class DailyMessagesTests(APITestCase):
    
    def setUp(self):
        """
        Create user objects for Daily Messages Tests
        """
        self.user = User.objects.create_user(username='user', password='123')
        self.client.force_authenticate(user=self.user)

    def test_get_daily_messages(self):
        """
        Successful GET Daily Messages
        """ 
        response = self.client.get(Paths.DAILY_MESSAGE , {'date' : '2020-09-27'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_daily_messages_invalid_data(self):
        """
        GET Daily Messages with Invalid Query Date String
        """
        response = self.client.get(Paths.DAILY_MESSAGE , {'date' : 'not_date'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_get_daily_messages_missing_data(self):
        """
        GET Daily Messages with Missing Query Date String
        """
        response = self.client.get(Paths.DAILY_MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

class PermissionTests(APITestCase):

    def test_permission_message(self):
        """
        GET Not Authenticated User Messages Test
        """
        response = self.client.get(Paths.MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_permission_received_message(self):
        """
        GET Not Authenticated User received Messages Test
        """ 
        response = self.client.get(Paths.RECEIVED_MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_permission_sent_message(self):
        """
        GET Not Authenticated User Sent Messages Test
        """ 
        response = self.client.get(Paths.SENT_MESSAGE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_permission_chat_message(self):
        """
        GET Not Authenticated User chat Messages Test
        """ 
        response = self.client.get(Paths.CHAT_MESSAGE, {'target': 'target_user'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_permission_daily_message(self):
        """
        GET Not Authenticated User daily Messages Test
        """ 
        response = self.client.get(Paths.DAILY_MESSAGE, {'date':'2020-01-01'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)