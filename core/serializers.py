from rest_framework import serializers
from .models import EstacionMeteorologica

class EstacionMeteorologicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstacionMeteorologica
        fields = '__all__'