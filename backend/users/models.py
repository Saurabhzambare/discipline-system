"""
models.py

This file defines database models for the users app.
Here we create a custom User model for the Discipline System.
"""

# Import Django's built-in base user class
# AbstractUser already includes common authentication fields
# like username, password, email, first_name, last_name, etc.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model for the Discipline System.

    We extend Django's AbstractUser instead of using the default User model.
    This gives us flexibility to add custom fields later without needing
    complicated database migrations.

    AbstractUser already includes these fields:
        - username
        - email
        - password
        - first_name
        - last_name
        - is_active
        - is_staff
        - is_superuser
        - last_login
        - date_joined
    """

    # Currently we are not adding any additional fields.
    # The `pass` statement simply means:
    # "Use all the default fields from AbstractUser for now."
    pass