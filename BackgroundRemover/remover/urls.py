from django.urls import path, include
from .api import BackgroundRemoverAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BackgroundRemoverAPI.as_view(), name='api-background-remover')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)