from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializer import *
from bs4 import BeautifulSoup as bs
from rest_framework import generics
from .scraper import *

# Create your views here.

class CarsCreateAPIView(generics.CreateAPIView):
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

                    # Create Foreign Keys if they don't exist.
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

# class CarsListAPIView(generics.RetrieveAPIView):
class CarsListAPIView(generics.ListAPIView):
    queryset = SearchedURLModel.objects.all()
    serializer_class = SearchedURLSerializer
    depth = 2

    def get_queryset(self):
        queryset = Car.objects.all()
        pk = self.request.query_params.get('pk')
        if pk is not None:
            queryset = queryset.filter(searched_url=pk)
        return queryset

        # return super().get_queryset().filter(id=self.kwargs['pk'])

        # objects = Car.objects.filter(searched_url=self.kwargs['pk']).all()
        # return objects
