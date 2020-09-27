from rest_framework.test import APITestCase, force_authenticate 
from rest_framework import status
from django.contrib.auth.models import User

class Paths:
    EXCEPTION = 'http://localhost:8000/api/exception'

class PermissionTests(APITestCase):

    def test_get_login_activities(self):
        """
        Forbidden GET Expception List Test (only admin users)
        """
        self.user = User.objects.create_user(username='test', password='123')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(Paths.EXCEPTION)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)