from django.urls import path, include
from . import views

urlpatterns = [
    path('create', views.CarsCreateAPIView.as_view()),
    path('view/<int:pk>', views.CarsListAPIView.as_view()),
]
