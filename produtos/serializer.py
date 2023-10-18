from .models import Produto
from rest_framework import serializers


class PodutoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Produto
        fields = '__all__'
