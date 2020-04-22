from django.urls import path
from .views import UserView

urlpatterns = [
    path('/member/join', UserView.as_view()),
]
