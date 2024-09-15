from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model representing a user in the system.

    Attributes:
        phone_number (str): The phone number of the user.
        email (str): The email address of the user. Can be blank or null.
    """
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)

class Contact(models.Model):
    """
    Represents a contact in the system.

    Attributes:
        owner (User): The owner of the contact.
        name (str): The name of the contact.
        phone_number (str): The phone number of the contact.
        is_spam (bool): Indicates whether the contact is marked as spam or not.
    """

    owner = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_spam = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('owner', 'phone_number')
