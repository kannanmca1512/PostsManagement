from django.core.management.base import BaseCommand
from social_app.models import AppUser 
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "initialize the vehicle library"
    
    def handle(self, *args, **kwargs):
        print("initializing .....1")
        self.create_admin()
        
    def create_admin(self):
        user = AppUser(
            password=make_password(settings.DEFAULT_ADMIN_PASSWORD),
            is_superuser=True,
            username="admin",
            first_name="Super",
            last_name="Admin",
            email="kannanbalakrishnan71@gmail.com",
            is_staff=True,
            is_active=True,
            date_joined=timezone.now())
        user.save()
        print("admin created")
        