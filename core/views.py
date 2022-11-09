from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import SearchedURLModel
from bs4 import BeautifulSoup as bs
from rest_framework import generics
from .scraper import *

# Create your views here.

class CarsCreateAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = SearchedURLModel

    def perform_create(self, serializer):
            user_url = serializer.validated_data.get('url')
            user_url_id = serializer.validated_data.get('id')

            if user_url is not None:

                cars_dict = DownloadPage(url=user_url).start()

                for key in cars_dict:
                    print(key, '->', cars_dict[key])

                serializer.save()

                for car in cars_dict.items():
                    smd = ScrapMoreData()
                    brand = smd.extractDataFromURL(url=car[1])
                    price = int(str(car[0]).replace(' ', ''))
                    url = car[1]
                    result = smd.start(price=car[0], url=car[1])

                    car_object = Car(car_url=user_url_id,
                                     brand=brand,
                                     year=int(result.get("Rok produkcji")),
                                     version=result.get("Wersja"),
                                     horsepower=int(result.get('Moc').replace(" KM", "")),
                                     doors=int(result.get('Liczba drzwi')),
                                     fuel=result.get('Rodzaj paliwa'),
                                     capacity=int(result.get('Pojemność skokowa').replace(" cm3", "").replace(" ", "")),
                                     gearbox=result.get('Skrzynia biegów'),
                                     bodytype=result.get('Typ nadwozia'),
                                     color=result.get('Kolor')
                                     )
                    car_object.save()

# class CarsListAPIView(generics.) #TODO create a list view, user gives a ID and gets a list of his you know
