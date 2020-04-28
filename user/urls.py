from django.urls import path
from .views import UserView, UserCheckView, SignInView

urlpatterns = [
    path('sign-up', UserView.as_view()),
    path('sign-up/check', UserCheckView.as_view()),
    path('sign-in', SignInView.as_view()),
]
