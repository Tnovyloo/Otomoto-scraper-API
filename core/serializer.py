from rest_framework import serializers
from .models import *

class SearchedURLSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SearchedURLModel
        fields = ['url']
