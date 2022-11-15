from rest_framework import serializers
from .models import *

# class SearchedURLSerializer(serializers.ModelSerializer):
#     # id = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = SearchedURLModel
#         fields = ['url']

# serializers.HyperlinkedModelSerializer
# class SearchedURLSerializer(serializers.HyperlinkedModelSerializer):
#     # id = serializers.IntegerField(read_only=True)
#     car = serializers.CharField(read_only=True, source='__all__')
#
#     class Meta:
#         model = SearchedURLModel
#         fields = ['url', 'car']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"

class SearchedURLSerializer(serializers.HyperlinkedModelSerializer):
    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = SearchedURLModel
        fields = ['url', 'cars']


# class CarsURLSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car
#         fields = "__all__"
