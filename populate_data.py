import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spam_checker.settings')
django.setup()

from contacts.models import User, Contact

faker = Faker()

def populate_users_and_contacts(num_users=10, num_contacts_per_user=5):
    for _ in range(num_users):
        user = User.objects.create_user(
            username=faker.user_name(),
            password='password123',
            phone_number=faker.phone_number(),
            email=faker.email()
        )
        for _ in range(num_contacts_per_user):
            Contact.objects.create(
                owner=user,
                name=faker.name(),
                phone_number=faker.phone_number(),
                is_spam=random.choice([True, False])
            )

if __name__ == "__main__":
    populate_users_and_contacts()
    print("Sample data populated.")
