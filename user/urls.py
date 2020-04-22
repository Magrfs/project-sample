from django.urls import path
from .views import UserView #CheckSignUpIdView

urlpatterns = [
    path('sign-up', UserView.as_view()),
    #path('sign-up/check', CheckSignUpIdView.as_view()),
]
