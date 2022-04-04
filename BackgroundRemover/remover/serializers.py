from rest_framework import serializers
from .models import TheImages

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheImages
        fields = '__all__'