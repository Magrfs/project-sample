import json
import bcrypt
import jwt
import re

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import User
from project_garam.settings import SECRET_KEY, ALGORITHM

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if len(data.keys()) == 1:
                if len(re.findall(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ&$ %\s]{0,0}", data['user_id'])) > 0:
                    return JsonResponse({"message": "INVALID_ID"}, status=400)

                if User.objects.filter(user_id=data['user_id']).exists():
                    return JsonResponse({"message": "DUPLICATE_ID"}, status=409)
                return JsonResponse({"message": "CHECK_ID_COMPLETE"}, status=200)

            if re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@.#^* ?+=_~])[A-Za-z\d!@.#^* ?+=_~]{8,}$", data['password']):
                hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                return HttpResponse(status=200)
            return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            
            if User.objects.fileter(phone=data['phone']).exists():
                return JsonResponse({"message": "DUPLICATE_PHONE_NUMBER"}, status=400)

            if len(data['name']) == 0:
                return JsonResponse({"message": "INPUT_NAME"}, status=401)

            if len(data['birthday']) == 0:
                return JsonResponse({"message": "INPUT_DATE"}, status=401)

            if len(data['phone']) == 0:
                return JsonResponse({"message": "INPUT_NUMBER"}, status=401)

            User.objects.create(
                user_id = data['user_id'],
                password = data['password'].decode('utf-8'),
                name = data['name'],
                birth_date = data['birth_date'],
                phone = data['phone'],
                email = data['email'],
                address = data['address'],
                address_detail = data['address_detail'],
            )
            return HttpResponse(status=200)

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