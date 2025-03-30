from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import Throttled

def api_exception_handler(exc, context):
     response = exception_handler(exc, context)
     
     if isinstance(exc, Http404):
          return Response({"error":"Resource not found."}, status=status.HTTP_404_NOT_FOUND)
     elif isinstance(exc, ValueError):
          return Response({"error":"Invalid input."}, status=status.HTTP_400_BAD_REQUEST)
     elif isinstance(exc, PermissionDenied):
          return Response({"error":"Permission denied."}, status=status.HTTP_403_FORBIDDEN)
     elif isinstance(exc, Throttled):
          return Response({"error":"Request was throttled."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
     
     return response