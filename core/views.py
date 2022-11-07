from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import SearchedURLModel
from bs4 import BeautifulSoup
from rest_framework import generics

# Create your views here.

class CarsCreateAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = SearchedURLModel

    def perform_create(self, serializer):
            user_url = serializer.validated_data.get('url')
            if user_url is not None:

                # TODO Create there a functions to scrap cars data and save it to database.
                # Create own id of searched user GET and tag a cars to it.

                serializer.save()
