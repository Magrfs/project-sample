from django.urls import path
from .views import UserView, SignInView #CheckSignUpIdView

urlpatterns = [
    path('sign-up', UserView.as_view()),
    path('sign-up/check', UserView.as_view()),
    path('sign-in', SignInView.as_view()),
]
