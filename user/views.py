import json
import bcrypt
import jwt
import re

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError

from .models import User
from project_garam.settings import SECRET_KEY, ALGORITHM
# from .utils import login_decorator

# def invalid_user(self, request):
#     pattern_user_id = r"[ㄱ-ㅎ가-힣ㅏ-ㅣ&$ %\s]"
#     pattern_password = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$"
#     pattern_birth = r"(\d{4})-(\d{2})-(\d{2})"
#     pattern_email = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

#     return re.match()

#     if data['{}'] if None or len(data{'{}'}) == 0:
#         return JsonResponse({"message": "INVALIDE_INPUT"}, status=400)
    
#     def invalid_id(self, ):



# class UserView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             if len(data.keys()) == 1:
#                 if len(re.findall(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ&$ %\s]", data['user_id'])) > 0 or len(data['user_id']) == 0:
#                     return JsonResponse({"message": "INVALID_ID"}, status=400)

#                 if User.objects.filter(user_id=data['user_id']).exists():
#                     return JsonResponse({"message": "DUPLICATE_ID"}, status=409)
#                 return HttpResponse(status=200)

#             if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$", data['password']):
#                 return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
#             hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

#             if data['name'] is None or len(data['name']) == 0:
#                 return JsonResponse({"message": "INPUT_NAME"}, status=400)

#             if data['birth_date'] is None or len(data['birth_date']) == 0:
#                 return JsonResponse({"message": "INPUT_DATE"}, status=400)

#             if not re.match(r"(\d{4})-(\d{2})-(\d{2})", data['birth_date']):
#                 return JsonResponse({"message": "INVALID_TIME"}, status=400)

#             if User.objects.filter(phone=data['phone']).exists():
#                 return JsonResponse({"message": "DUPLICATE_PHONE_NUMBER"}, status=409)

#             if data['phone'] is None or len(data['phone']) == 0:
#                 return JsonResponse({"message": "INPUT_NUMBER"}, status=400)

#             if data['email'] is None or len(data['email']) == 0 or not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data['email']):
#                 return JsonResponse({"message": "INPUT_MAIL_ADDRESS"}, status=400)
#             if User.objects.filter(email=data['email']).exists():
#                 return JsonResponse({"message": "DUPLICATE_EMAIL"}, status=400)

#             User.objects.create(
#                 user_id = data['user_id'],
#                 password = hashed_password.decode('utf-8'),
#                 name = data['name'],
#                 birth_date = data['birth_date'],
#                 phone = data['phone'],
#                 email = data['email'],
#                 address = data.get('address', None),
#                 )
#             return HttpResponse(status=200)

#         except KeyError:
#             return JsonResponse({"message": "INVALID_KEYS"}, status=400)


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
            'user_id' : lambda user_id : False if User.objects.filter(user_id=user_id).exists() else True,
            'password' : lambda password : False if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$",password) else True,
            'name' : lambda name : False if name is None or len(name) == 0 else True,
            'birth_date' : lambda birth_date : False if not re.match(r"(\d{4})-(\d{2})-(\d{2})", birth_date) else True,
            'phone' : lambda phone : False if User.objects.filter(phone=phone).exists() else True,
            'email' : lambda email : False if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) else True
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

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(user_id = data['user_id']).exists():
                user = User.objects.get(user_id = data['user_id'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
                    return JsonResponse({"token:": token}, status=200)
                return HttpResponse(status=401)
            return HttpResponse(status=401)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

# class UserChangeView(View):
#     @login_decorator
#     def post(self, request):
#         data = json.loads(request.body)
#         try:
#             if len(data.keys()) == 2:
#                 if User.objects.filter(user_id=data['user_id']).exists():
#                     user = User.objects.get(user_id = data['user_id'])

#                     if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
#                         return HttpResponse(status=200)
#                     return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

#             if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$", data['password']):
#                 return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
#             hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

#             if User.objects.filter(phone=data['phone']).exists():
#                 return JsonResponse({"message": "DUPLICATE_PHONE_NUMBER"}, status=409)

#             if data['email'] is None or len(data['email']) == 0 or not re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
#                 return JsonResponse({"message": "INPUT_MAIL_ADDRESS"}, status=400)

#             User.objects.update(
#                 password = hashed_password.decode('utf-8'),
#                 phone = data['phone'],
#                 email = data['email'],
#                 address = data.get('address', None),
#                 )
#             return HttpResponse(status=200)

#         except KeyError:
#             JsonResponse({"message": "INVALID_KEYS"}, status=400)