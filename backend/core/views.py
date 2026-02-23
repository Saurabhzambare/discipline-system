from django.shortcuts import render
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore

# Create your views here.


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "service": "discipline-system-api"})
