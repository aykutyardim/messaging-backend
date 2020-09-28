from rest_framework.test import APITestCase, force_authenticate 

from rest_framework import status
from django.contrib.auth.models import User

from accounts.models import LoginActivity, Block
from exceptions.models import ExceptionModel

class Paths:

    REGISTER = 'http://localhost:8000/api/auth/register'
    LOGIN = 'http://localhost:8000/api/auth/login'
    BLOCK = 'http://localhost:8000/api/block'
    USER = 'http://localhost:8000/api/auth/user'
    LOGINACTIVITY ='http://localhost:8000/api/auth/loginactivity'

class Constants:
    CREDENTIALS = {'username' : 'test', 'password' : '123'}


class RegisterTests(APITestCase):

    def test_resgister(self):
        """
        Successful Registration Test
        """
        response = self.client.post(Paths.REGISTER, Constants.CREDENTIALS)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        
    def test_register_invalid_data(self):
        """
        Registration Tests with Invalid Duplicated Data
        """
        User.objects.create_user(username='test', password='123')
        response = self.client.post(Paths.REGISTER, Constants.CREDENTIALS)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_register_missing_data(self):
        """
        Registration Test with Missing Data 
        """
        response = self.client.post(Paths.REGISTER)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        users = User.objects.all()
        self.assertEqual(users.count(), 0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)


class LoginTests(APITestCase):       
    
    def test_login(self):
        """
        Successful Login Tests
        """
        User.objects.create_user(username='test', password='123')
        response = self.client.post(Paths.LOGIN, Constants.CREDENTIALS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        activities = LoginActivity.objects.all() 
        self.assertEqual(activities.count(), 1)

    def test_login_invalid_data(self):
        """
        Login Tests with Invalid Credential
        """
        response = self.client.post(Paths.LOGIN, Constants.CREDENTIALS)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        activities = LoginActivity.objects.all() 
        self.assertEqual(activities.count(), 1)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_login_missing_data(self):
        """
        Login Tests with Missing Data
        """
        response = self.client.post(Paths.LOGIN)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)


class BlockTests(APITestCase):
    
    def setUp(self):
        """
        Create user objects for Blocking tests
        """
        self.prevented = User.objects.create_user(username='prevented_user', password='123')
        self.blocked = User.objects.create_user(username='blocked_user', password='123')
        self.client.force_authenticate(user=self.prevented)

    def test_get_block(self):
        """
        Successful GET Block List Test
        """
        response = self.client.get(Paths.BLOCK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_block(self):
        """
        Successful POST Block Test
        """
        response = self.client.post(Paths.BLOCK, {'blocked' : 'blocked_user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blocks = Block.objects.filter(prevented=self.prevented, blocked=self.blocked)
        self.assertEqual(blocks.count(),1)

    def test_post_block_client_data(self):
        """
        POST Block Test with client Blocked Field
        """
        response = self.client.post(Paths.BLOCK, {'blocked' : 'prevented_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        blocks = Block.objects.all()
        self.assertEqual(blocks.count(),0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)
    
    def test_post_block_invalid_data(self):
        """
        POST Block Test with Invalid Blocked Field
        """
        response = self.client.post(Paths.BLOCK, {'blocked' : 'not_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        blocks = Block.objects.all()
        self.assertEqual(blocks.count(),0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)
    
    def test_post_block_dublicated_data(self):
        """
        POST Block Test with dublicated Blocked Field
        """
        Block.objects.create(prevented=self.prevented, blocked=self.blocked)
        response = self.client.post(Paths.BLOCK, {'blocked' : 'blocked_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        blocks = Block.objects.all()
        self.assertEqual(blocks.count(),1)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_post_block_missing_data(self):
        """
        POST Block Test with Missing Blocked Field
        """
        response = self.client.post(Paths.BLOCK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        blocks = Block.objects.all()
        self.assertEqual(blocks.count(),0)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_delete_block(self):
        """
        Successful Delete Block Test
        """
        Block.objects.create(prevented=self.prevented, blocked=self.blocked)
        response = self.client.delete(Paths.BLOCK, {'blocked' : 'blocked_user'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        blocks = Block.objects.all()
        self.assertEqual(blocks.count(),0)

    def test_delete_not_existing(self):
        """
        Delete Not existing Block Test
        """
        response = self.client.delete(Paths.BLOCK, {'blocked' : 'blocked_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_delete_block_client_data(self):
        """
        Delete Block Test with client Blocked Field
        """
        response = self.client.delete(Paths.BLOCK, {'blocked' : 'prevented_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)
    
    def test_delete_block_invalid_data(self):
        """
        Delete Block Test with Invalid Blocked Field
        """
        response = self.client.delete(Paths.BLOCK, {'blocked' : 'not_user'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)

    def test_delete_block_missing_data(self):
        """
        Delete Block Test with Missing Blocked Field
        """
        response = self.client.delete(Paths.BLOCK)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exceptions = ExceptionModel.objects.all()
        self.assertEqual(exceptions.count(), 1)


class UserTests(APITestCase):
    
    def setUp(self):
        """
        Create user objects for User tests
        """
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_authenticate(user=self.user)

    def test_get_user(self):
        """
        Successful GET Authenticated User Test
        """
        response = self.client.get(Paths.USER)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), 'test')


class PermissionTests(APITestCase):

    def test_get_not_auth(self):
        """
        GET Not Authenticated User Test
        """
        response = self.client.get(Paths.USER)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)        

    def test_get_login_activities(self):
        """
        Forbidden GET Login Activities List Test (only admin users)
        """
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(Paths.LOGINACTIVITY)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)