from django.conf import settings
from django.forms import ImageField
from django.core.files.uploadedfile import UploadedFile
from drf_extra_fields.fields import Base64FieldMixin, Base64FileField, Base64ImageField
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from rest_framework.fields import FileField, SkipField

__all__ = (
    'NamedBase64FieldMixin',
    'NamedBase64FileField',
    'NamedBase64ImageField',
)


class NamedBase64FieldMixin(Base64FieldMixin):
    INVALID_OBJECT = 'Must be an object containing keys "file_name" and "encoded_str"'
    INVALID_DATA = '"URL starting with http" or "Object with file_name and encoded_str must be passed"'
    INVALID_FILE_NAME = 'The file name is incorrect. It should have the form "<name>.<extension>"'
    INVALID_FILE_UPLOAD = 'The file uploaded directly is invalid, must have a name and size'
    ALLOWED_TYPES = [
        'jpeg',
        'jpg',
        'png',
        'gif',
    ]
    ALLOW_ALL_EXTENSIONS = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.help_text is None:
            self.help_text = 'Object containing the base64-encoded file along with the name'

    def to_internal_value(self, obj):
        if obj in self.EMPTY_VALUES:
            return None
        elif isinstance(obj, str):
            if obj.startswith('http'):
                raise SkipField()
            media_url = getattr(settings, 'MEDIA_URL', None)
            if media_url and obj.startswith(media_url):
                raise SkipField()
        elif isinstance(obj, dict):
            if not all(key in obj for key in ('file_name', 'encoded_str')):
                raise ValidationError(self.INVALID_OBJECT)
            try:
                self.name, self.ext = obj['file_name'].rsplit('.', 1)
            except ValueError:
                raise ValidationError(self.INVALID_FILE_NAME)

            if self.ext not in self.ALLOWED_TYPES and self.ALLOW_ALL_EXTENSIONS:
                self.ALLOWED_TYPES.append(self.ext)

            encoded_str = obj['encoded_str']
            return super().to_internal_value(encoded_str)
        elif isinstance(obj, UploadedFile):
            try:
                self.name = obj.name
                self.size = obj.size
            except AttributeError:
                raise ValidationError(self.INVALID_FILE_UPLOAD)

            try:
                _, self.ext = self.name.rsplit('.', 1)
            except ValueError:
                raise ValidationError(self.INVALID_FILE_NAME)

            if self.ext not in self.ALLOWED_TYPES and not self.ALLOW_ALL_EXTENSIONS:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)

            return obj
        else:
            raise ValidationError(self.INVALID_DATA)

    def get_file_name(self, decoded_file):
        return self.name

    def get_file_extension(self, filename, decoded_file):
        return self.ext

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'read_only': False,
            'properties': {
                'file_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=r'Uploaded file name with the form **`<name>.<extension>`**',
                    example='pby.jpg',
                ),
                'encoded_str': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Base64 encoded file string',
                    example='aHR0cHM6Ly9naXRodWIuY29tL2xlZWhhbnllb25n',
                ),
            },
        }


class NamedBase64FileField(NamedBase64FieldMixin, Base64FileField, FileField):
    ALLOW_ALL_EXTENSIONS = True


class NamedBase64ImageField(NamedBase64FieldMixin, Base64ImageField, ImageField):
    ALLOW_ALL_EXTENSIONS = True
