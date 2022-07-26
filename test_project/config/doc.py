from drf_yasg import openapi
from drf_yasg.renderers import ReDocRenderer, OpenAPIRenderer
from drf_yasg.views import get_schema_view
from rest_framework import permissions

BaseSchemaView = get_schema_view(
    openapi.Info(
        title="drf-base64-filename",
        default_version="v1",
        description="drf-base64-filename drf-yasg",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


class ReDocSchemaView(BaseSchemaView):
    renderer_classes = (ReDocRenderer, OpenAPIRenderer)
