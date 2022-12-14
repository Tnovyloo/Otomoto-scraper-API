from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import *
from bs4 import BeautifulSoup as bs
from rest_framework import generics
from .scraper import *
from django.db.models import Subquery
from django.http import JsonResponse
from rest_framework.response import Response
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.

class CarsCreateAPIView(generics.CreateAPIView):
    """When user provides a 'Otomoto' URL, the API scraps all cars and
    their own data to database."""
    queryset = Car.objects.all()
    serializer_class = SearchedURLSerializer

    def perform_create(self, serializer, *args, **kwargs):
            user_url = serializer.validated_data.get('url')

            if user_url is not None:

                cars_dict = DownloadPage(url=user_url).start()

                for key in cars_dict:
                    print(key, '->', cars_dict[key])

                data_id = serializer.save()
                user_url_obj = SearchedURLModel.objects.get(pk=data_id.id)

                for car in cars_dict.items():
                    smd = ScrapMoreData()
                    brand = smd.extractDataFromURL(url=car[1])
                    price = int(str(car[0]).replace(' ', ''))
                    car_url = car[1]
                    result = smd.start(price=car[0], url=car[1])

                    # Create Foreign Keys if they still doesn't exist.
                    if Brand.objects.filter(brand=brand).exists() is False:
                        new_brand = Brand.objects.create(brand=brand)
                        new_brand.save()

                    if Fuel.objects.filter(fuel_type=result.get('Rodzaj paliwa')).exists() is False:
                        new_fuel = Fuel.objects.create(fuel_type=result.get('Rodzaj paliwa'))
                        new_fuel.save()

                    if Gearbox.objects.filter(gearbox_type=result.get('Skrzynia biegów')).exists() is False:
                        new_gearbox = Gearbox.objects.create(gearbox_type=result.get('Skrzynia biegów'))
                        new_gearbox.save()

                    if BodyType.objects.filter(bodytype=result.get('Typ nadwozia')).exists() is False:
                        new_bodytype = BodyType.objects.create(bodytype=result.get('Typ nadwozia'))
                        new_bodytype.save()

                    if Color.objects.filter(color=result.get('Kolor')).exists() is False:
                        new_color = Color.objects.create(color=result.get('Kolor'))
                        new_color.save()

                    brand_obj = Brand.objects.get(brand=brand)
                    fuel_obj = Fuel.objects.get(fuel_type=result.get('Rodzaj paliwa'))
                    gearbox_obj = Gearbox.objects.get(gearbox_type=result.get('Skrzynia biegów'))
                    bodytype_obj = BodyType.objects.get(bodytype=result.get('Typ nadwozia'))
                    color_obj = Color.objects.get(color=result.get('Kolor'))

                    car_object = Car(searched_url=user_url_obj,
                                     price=price,
                                     car_url=car_url,
                                     brand=brand_obj,
                                     body_type=bodytype_obj,
                                     gearbox=gearbox_obj,
                                     color=color_obj,
                                     fuel=fuel_obj,
                                     model=result.get('Model pojazdu'),
                                     year=int(result.get("Rok produkcji")),
                                     version=result.get("Wersja"),
                                     capacity=int(result.get('Pojemność skokowa').replace(" cm3", "").replace(" ", "")),
                                     horsepower=int(result.get('Moc').replace(" KM", "")),
                                     doors=int(result.get('Liczba drzwi')),
                                     )
                    car_object.save()
                return Response()

class CarsListAPIView(generics.ListAPIView):
    """While getting a PK it returns all cars with data where the
        'PK' was the same (Primary key is once per searched url.)
        """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_field)
        print(pk)
        if pk is not None:
            queryset = self.queryset.filter(searched_url=pk)
            return queryset
        return None


