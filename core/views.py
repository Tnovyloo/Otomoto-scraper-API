from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import URLSerializer
from bs4 import BeautifulSoup
from rest_framework import generics

# Create your views here.

class CarsCreateAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = SearchedURLModel

    # def perform_create(self, serializer):
    #
    #     # serializer.save(user=self.request.user)
    #     title = serializer.validated_data.get('title')
    #     content = serializer.validated_data.get('content') or None
    #     if content is None:
    #         content = title
    #
    #     serializer.save()