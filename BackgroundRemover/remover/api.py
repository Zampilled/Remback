from django.shortcuts import render
# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import ImageSerializer
from AI.removerscript import image
from .models import TheImages

class BackgroundRemoverAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ImageSerializer
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        img = TheImages.objects.create(image=data['image'])
        foreground = image(img.image.path, img.image.name)
        img.delete()
        return Response({
            'image': foreground
        })


