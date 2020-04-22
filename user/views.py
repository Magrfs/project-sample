import json
import bcrypt
import jwt
import re

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import User
from project_garam.settings import SECRET_KEY


class UserView():
    def post(self, request):
        data = json.loads(request.body)
        try:
            if len(json.keys()) == 1:
                # 공백 \s
                # 숫자 \d
                # 한글 ㄱ-ㅎ가-힣ㅏ-ㅣ
                # &$%
                # 아이디에 한글 또는 특수문자(&$%)/공백은 사용할수 없습니다.
                if len(re.findall(r"[ㄱ-ㅎ가-힣ㅏ-ㅣ&$%\s]", data['user_id'])) > 0:
                    return JsonResponse({"message": "INVALID_ID"}, status=400)

                if User.objects.filter(user_id=data['user_id']).exists():
                    return JsonResponse({"message": "DUPLICATE_ID"}, status=409)
                return JsonResponse({"message": "ID_CHECK_COMPLETE"}, status=200)

            # 영문자/숫자/특수 문자가 모두 포함되어야 합니다. 사용 가능한 특수 문자는 !@.#^* ?+=_~ 입니다. 비밀번호는 최소 8자리 이상입니다. 공백은 사용하실 수 없습니다.
            if len(re.findall(r"[^A-Za-z0-9!@.#^* ?+=_~]", data['password'])) > 0 or len(data['password']) < 8:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            hashed_password = bcrypt.hashpw(
                data['password'].encode('utf-8'), bcrypt.gensalt())

            if User.objects.fileter(phone=data['phone']).exists():
                return JsonResponse({"message": "DUPLICATE_PHONE_NUMBER"}, status=400)

            # if data['name'] == NULL:
            #     return JsonResponse({"message": "이름내놔"}, status=400)

            # if data['birthday'] = :
            #     return JsonResponse({"message": "생일내놔"}, status=400)

            # if data['phone'] = NULL:
            #     return JsonResponse({"message": "전화번호내놔"}, status=400)

            User.objects.create(
                user_id=data['user_id']
                password=data['user_id']
                name=data['name']
                birthday=data['birthday']
                phone=data['phone']
                email=data['email']
                address=data['address']
            )
            return HttpResponse(status=200)

            except KeyError:
                return JsonResponse({"message": "INVALID_KEYS"}, status=400)
