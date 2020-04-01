from django.forms import ImageField
from drf_extra_fields.fields import Base64FieldMixin, Base64ImageField, Base64FileField
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
            self.help_text = 'An object containing keys `file_name` and `encoded_str`'

    def to_internal_value(self, obj):
        if obj in self.EMPTY_VALUES:
            return None
        elif isinstance(obj, str) and obj.startswith('http'):
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
        else:
            raise ValidationError(self.INVALID_DATA)

    def get_file_name(self, decoded_file):
        return self.name

    def get_file_extension(self, filename, decoded_file):
        return self.ext


class NamedBase64FileField(NamedBase64FieldMixin, Base64FileField, FileField):
    ALLOW_ALL_EXTENSIONS = True


class NamedBase64ImageField(NamedBase64FieldMixin, Base64ImageField, ImageField):
    ALLOW_ALL_EXTENSIONS = True
