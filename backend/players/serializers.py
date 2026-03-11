"""
serializers.py

This file contains serializers for the players app.

A serializer converts Django model objects into JSON
so they can be returned through API responses.
"""

# Import Django REST Framework serializer tools
from rest_framework import serializers

# Import the Player model
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model.

    ModelSerializer automatically generates serializer fields
    based on the fields defined in the model.
    """

    # ---------------------------------------------------------
    # EXTRA FIELD FROM RELATED MODEL
    # ---------------------------------------------------------
    # The Player model does not store the username directly.
    # Username exists in the related User model.
    #
    # source="user.username" tells DRF to get the value from:
    # Player → user → username
    #
    # read_only=True means the API will return this value,
    # but clients cannot modify it through this serializer.
    username = serializers.CharField(source="user.username", read_only=True)


    class Meta:
        """
        The Meta class tells the serializer how to behave.
        """

        # Specify which model this serializer represents
        model = Player

        # List of fields to include in the API response
        fields = [
            "id",          # Primary key of the Player record
            "username",    # Username from related User model
            "level",       # Player's current level
            "exp",         # Player's experience points
            "streak",      # Player's current streak
            "created_at",  # Timestamp when player profile was created
            "updated_at",  # Timestamp of last update
        ]