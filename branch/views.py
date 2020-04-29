from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import Area, Branch, Region


class AreaView(View):
    def get(self, request, target_code=''):
        try:
            region_code = target_code[:1]
            region = Region.objects.prefetch_related('area_set__branch_set').get(code=region_code)
            
            area_info = [
                {
                    "area_name" : area.name,
                    "area_code" : area.code,
                    "clickable" : area.branch_set.exists()
                } for area in region.area_set.all()
            ]
            return JsonResponse({"area_info": area_info}, status=200)
        except Region.DoesNotExist:
            return HttpResponse(status=404)