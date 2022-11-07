from django.db import models

# Create your models here.

class CarURLModel(models.Model):
    models.URLField(max_length=1500)

class Brand(models.Model):
    models.CharField(max_length=255)

class Fuel(models.Model):
    models.CharField(max_length=5)

class Gearbox(models.Model):
    models.CharField(max_length=100)

class BodyType(models.Model):
    models.CharField(max_length=100)

class Color(models.Model):
    models.CharField(max_length=100)

class Car(models.Model):
    car_url = models.ForeignKey(CarURLModel, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    gearbox = models.ForeignKey(Gearbox, on_delete=models.CASCADE)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    year = models.IntegerField(null=False)
    version = models.CharField(max_length=100)
    horsepower = models.IntegerField()
    doors = models.IntegerField()
    capacity = models.IntegerField()

class SearchedURLModel(models.Model):
    models.ForeignKey(Car, on_delete=models.CASCADE)