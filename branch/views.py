from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import Branch


class StoreView(View):
    def get(self, request):
        pass