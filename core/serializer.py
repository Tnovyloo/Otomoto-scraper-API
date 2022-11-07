from rest_framework import serializers
from .models import *

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedURLModel
        fields = ('__all__')
