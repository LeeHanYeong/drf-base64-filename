from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors import FieldInspector, NotHandled

from drf_base64.fields import NamedBase64FieldMixin

__all__ = ("NamedBase64FieldInspector",)


class NamedBase64FieldInspector(FieldInspector):
    def field_to_swagger_object(
        self, field, swagger_object_type, use_references, **kwargs
    ):
        if issubclass(type(field), NamedBase64FieldMixin):
            properties = OrderedDict(
                file_name=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=r"Uploaded file name with the form **`<name>.<extension>`**",
                    example="pby.jpg",
                ),
                encoded_str=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Base64 encoded file string",
                    example="aHR0cHM6Ly9naXRodWIuY29tL2xlZWhhbnllb25n",
                ),
            )
            result = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties,
            )
            return result
        return NotHandled
