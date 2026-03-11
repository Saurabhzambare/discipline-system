"""
views.py

This file defines API endpoints (views) that respond to HTTP requests.
The 'health' endpoint is used to verify that the API server is running.
"""

from django.shortcuts import render  # Default Django import (not used here but often included)

from rest_framework.response import Response      # Used to send JSON responses
from rest_framework.decorators import api_view    # Converts a function into a DRF API view
from rest_framework.permissions import AllowAny   # Permission class allowing anyone to access
from rest_framework.decorators import permission_classes  # Used to apply permissions to a view


# ---------------------------------------------------------
# HEALTH CHECK ENDPOINT
# ---------------------------------------------------------
# This endpoint confirms that the backend API is alive.
#
# Example request:
# GET /api/health/
#
# Example response:
# {
#   "status": "ok",
#   "service": "discipline-system-api"
# }
#
# Used by:
# - Developers
# - Monitoring systems
# - Docker health checks
# - Load balancers
#

@api_view(["GET"])  # This view only accepts GET requests
@permission_classes([AllowAny])  # Anyone can access this endpoint (no authentication required)
def health(request):
    
    # Return a simple JSON response confirming the API is running
    return Response({
        "status": "ok",
        "service": "discipline-system-api"
    })