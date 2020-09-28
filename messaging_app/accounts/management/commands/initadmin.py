from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Initialize a superuser 
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            User.objects.get(is_superuser=True)
            print('Superuser is already exist')
        except ObjectDoesNotExist:
            username = 'admin'
            email = 'admin@messagingapp.com'
            password = '123'
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.save()
            print('Superuser is created')