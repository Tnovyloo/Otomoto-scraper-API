from django.db import models

# Create your models here.

class SearchedURLModel(models.Model):
    url = models.CharField(max_length=1500, default='None')

    def __str__(self):
        return f"Searched URL: {self.url}"

class Brand(models.Model):
    brand = models.CharField(max_length=255, default=None)

    def __str__(self):
        return str(self.brand).capitalize()

class Fuel(models.Model):
    fuel_type = models.CharField(max_length=5, default=None)

    def __str__(self):
        return str(self.fuel_type).upper()

class Gearbox(models.Model):
    gearbox_type = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.gearbox_type).capitalize()

class BodyType(models.Model):
    bodytype = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.bodytype).capitalize()

class Color(models.Model):
    color = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.color).capitalize()

class Car(models.Model):
    """car_url -> Foreign Key of Searched """
    car_url = models.CharField(max_length=2000)
    price = models.IntegerField(default=0)

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

    searched_url = models.ForeignKey(SearchedURLModel, on_delete=models.CASCADE, default="None")
