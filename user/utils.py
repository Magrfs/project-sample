import jwt
import json

from django.http import JsonResponse
from .models import User

from project_garam.settings import SECRET_KEY, ALGORITHM


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({"message": "INVALID_CLIENT_TOKEN"}, status=401)

        token = request.headers["Authorization"]

        try:
            data = jwt.decode(token, SECRET_KEY, ALGORITHM)
            user = User.objects.get(id=data['id'])
            request.user = user

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)
        except User.DoesNotExist:
            return JsonResponse({"message": "UNKNOWN_USER"}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper