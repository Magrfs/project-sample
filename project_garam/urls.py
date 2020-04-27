from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('store', include('branch.urls')),
]
