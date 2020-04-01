from django.urls import path, include

from .doc import ReDocSchemaView

urlpatterns = [
    path('doc/', ReDocSchemaView.as_cached_view(cache_timeout=0), name='schema-redoc'),
    path('', include('sample.urls')),
]
