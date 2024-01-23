from rest_framework import serializers
from .models import Island


class IslandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Island
        fields = '__all__'
