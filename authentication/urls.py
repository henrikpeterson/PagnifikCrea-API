from django.urls import path 
from .views import RegisterView, index

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('protected-route/', index)
]