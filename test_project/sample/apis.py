from rest_framework import viewsets

from .models import SampleBase64ImageModel, SampleBase64FileModel, SampleParentModel
from .serializers import (
    SampleBase64ImageSerializer,
    SampleBase64FileSerializer,
    SampleNamedBase64ImageSerializer,
    SampleNamedBase64FileSerializer,
    SampleParentFilenameImageSerializer,
    SampleParentFilenameFileSerializer,
)


class SampleBase64ImageViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64ImageModel.objects.all()
    serializer_class = SampleBase64ImageSerializer


class SampleBase64FileViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64FileModel.objects.all()
    serializer_class = SampleBase64FileSerializer


class SampleNamedBase64ImageViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64ImageModel.objects.all()
    serializer_class = SampleNamedBase64ImageSerializer


class SampleNamedBase64FileViewSet(viewsets.ModelViewSet):
    queryset = SampleBase64FileModel.objects.all()
    serializer_class = SampleNamedBase64FileSerializer


class SampleParentWithFilenameImageViewSet(viewsets.ModelViewSet):
    queryset = SampleParentModel.objects.all()
    serializer_class = SampleParentFilenameImageSerializer


class SampleParentWithFilenameFileViewSet(viewsets.ModelViewSet):
    queryset = SampleParentModel.objects.all()
    serializer_class = SampleParentFilenameFileSerializer
