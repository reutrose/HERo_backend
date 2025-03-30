from api.serializers import APITokenObtainPairSerializer
from rest_framework.authentication import SessionAuthentication


def get_tokens_for_user(user):
     refresh = APITokenObtainPairSerializer.get_token(user)
     return {
          'refresh': str(refresh),
          'access': str(refresh.access_token),
     }

class CsrfExemptSessionAuthentication(SessionAuthentication):
     def enforce_csrf(self, request):
          if request.content_type == "application/json":
               return
          return super().enforce_csrf(request)