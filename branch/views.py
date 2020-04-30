from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Area, Branch, Region


class AreaView(View):
    def get(self, request, target_code=''):
        try:
            region = Region.objects.prefetch_related('area_set__branch_set').get(code=target_code)
            
            area_info = [
                {
                    "area_name" : area.name.strip(),
                    "area_code" : area.code,
                    "clickable" : area.branch_set.exists()
                } for area in region.area_set.all()
            ]
            area_info.insert(0, {"area_name": "전체" , "area_code": target_code+"00", "clickable" : True})

            return JsonResponse({"area_info": area_info}, status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)