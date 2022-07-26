from django.urls import include, path
from rest_framework.routers import SimpleRouter

from sample import apis

router = SimpleRouter()
router.register(r"image", apis.SampleBase64ImageViewSet)
router.register(r"file", apis.SampleBase64FileViewSet)
router.register(r"image-name", apis.SampleNamedBase64ImageViewSet)
router.register(r"file-name", apis.SampleNamedBase64FileViewSet)
router.register(r"parent-image-name", apis.SampleParentWithFilenameImageViewSet)
router.register(r"parent-file-name", apis.SampleParentWithFilenameFileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
