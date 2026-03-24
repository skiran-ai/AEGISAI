from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Creates the default admin account if it does not exist'

    def handle(self, *args, **options):
        email = 'admin@gmail.com'
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin account "{email}" already exists.'))
            return

        CustomUser.objects.create_user(
            email=email,
            password='admin',
            first_name='Admin',
            last_name='AEGISAI',
            role=CustomUser.ADMIN,
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write(self.style.SUCCESS(f'Default admin account created: {email}'))
