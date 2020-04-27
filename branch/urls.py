from django.urls import path
from .views import UserView, StoreView

urlpatterns = [
    path('', UserView.as_view()),
    path('', StoreView.as_view()),
]
