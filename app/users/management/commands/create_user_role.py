from django.core.management.base import BaseCommand
from users.models import UserRole


class Command(BaseCommand):
    help = 'Create Data'

    def __init__(self):
        self.data_city_town = [
            UserRole(
                role='normal',
                name='Normal'
            ),
            UserRole(
                role='vip',
                name='Vip',
            )
        ]

    def handle(self, *args, **options):
        self.create_data()

    def create_data(self):
        UserRole.objects.bulk_create(self.data_city_town)
        print("Create User Role Done")
