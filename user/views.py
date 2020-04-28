import json
import bcrypt
import jwt
import re

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from .models import User


class UserCheckView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if len(re.findall(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ&$ %\s]", data['user_id'])) > 0 or len(data['user_id']) == 0:
                return JsonResponse({"message": "INVALID_ID"}, status=400)

            if User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({"message": "DUPLICATE_ID"}, status=409)
            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

class UserView(View):
    VALIDATION_RULES = {
        'user_id': lambda user_id: False if User.objects.filter(user_id=user_id).exists() else True,
        'password': lambda password: False if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$", password) else True,
        'name': lambda name: False if name is None or len(name) == 0 else True,
        'birth_date': lambda birth_date: False if not re.match(r"(\d{4})-(\d{2})-(\d{2})", birth_date) else True,
        'phone': lambda phone: False if User.objects.filter(phone=phone).exists() else True,
        'email': lambda email: False if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) else True
    }

    def post(self, request):
        try:
            data = json.loads(request.body)
            if len(data.keys()) < 6:
                return HttpResponse(status=400)
            for value in data.values():
                if value in "":
                    return HttpResponse(status=400)

            for field, validator in self.VALIDATION_RULES.items():
                if not validator(data[field]):
                    return HttpResponse(status=400)

            User.objects.create(
                user_id=data['user_id'],
                password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name=data['name'],
                birth_date=data['birth_date'],
                phone=data['phone'],
                email=data['email'],
                address=data.get('address', None),
            )
            return HttpResponse(status=200)

        except IntegrityError:
            return JsonResponse({"message": "DUPLICATED_KEYS"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)