from django.urls import path
from .views import AreaView

urlpatterns = [
    path('/<str:target_code>', AreaView.as_view()),
]
