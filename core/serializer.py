from rest_framework import serializers
from .models import *

class SearchedURLSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SearchedURLModel
        fields = ['url']

# class CarsURLSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Car
#         fields = "__all__"
