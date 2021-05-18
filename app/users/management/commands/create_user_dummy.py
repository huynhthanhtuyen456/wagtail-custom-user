from django.core.management.base import BaseCommand
from users.models import User

import uuid


class Command(BaseCommand):
    help = 'Create Data'

    def __init__(self):
        list_first_name = ['Malia', 'Meghan', 'Kirsten', 'Ryleigh', 'Ellis', 'Philip', 'Chandler', 'Asia', 'Deangelo',
                           'Luis', 'Kenny', 'Fatima', 'Riley', 'Jessie', 'Amina', 'John', 'Jessie', 'Callie', 'Allison',
                           'Hailie', 'Nevaeh', 'Madden', 'Juliet', 'Cadence', 'Zoey', 'Damon', 'Reuben', 'Elisa',
                           'Miracle', 'Eleanor']
        list_last_name = ['Duran', 'Sloan', 'Henderson', 'Browning', 'Ramos', 'Livingston', 'Bender', 'Allen',
                          'Rodriguez', 'Hammond', 'Campos', 'Jimenez', 'Mcintyre', 'Stafford', 'Hartman', 'Christensen',
                          'Romero', 'Keller', 'Foley', 'Hampton', 'Briggs', 'Benjamin', 'Mooney', 'Monroe', 'Rodriguez',
                          'Osborn', 'Ball', 'Oneal', 'York', 'Salinas']
        self.data_user_dummy = []
        email_refit = '@mailinator.com'
        for i in range(len(list_first_name)):
            email = list_first_name[i]+list_last_name[i]+email_refit
            print(email)
            self.data_user_dummy.append(User(email=email,
                                             first_name=list_first_name[i],
                                             last_name=list_last_name[i],
                                             username=email))

    def handle(self, *args, **options):
        self.create_data()

    def create_data(self):
        User.objects.bulk_create(self.data_user_dummy)
        users = User.objects.all()
        for user in users:
            user.save()
        print("Dummy User Done")
