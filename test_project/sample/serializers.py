from drf_extra_fields.fields import Base64ImageField, Base64FileField
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from drf_base64.fields import NamedBase64ImageField, NamedBase64FileField
from .models import SampleBase64ImageModel, SampleBase64FileModel, SampleParentModel


class SampleBase64ImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = SampleBase64ImageModel
        fields = (
            'id',
            'image',
        )


class SampleBase64FileSerializer(serializers.ModelSerializer):
    file = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = SampleBase64FileModel
        fields = (
            'id',
            'file',
        )


class SampleNamedBase64ImageSerializer(serializers.ModelSerializer):
    image = NamedBase64ImageField(required=False, allow_null=True)

    class Meta:
        model = SampleBase64ImageModel
        fields = (
            'id',
            'image',
        )


class SampleNamedBase64FileSerializer(serializers.ModelSerializer):
    file = NamedBase64FileField(required=False, allow_null=True)

    class Meta:
        model = SampleBase64FileModel
        fields = (
            'id',
            'file',
        )


class SampleParentFilenameImageSerializer(WritableNestedModelSerializer):
    image_set = SampleNamedBase64ImageSerializer(many=True)

    class Meta:
        model = SampleParentModel
        fields = (
            'id',
            'image_set',
        )


class SampleParentFilenameFileSerializer(WritableNestedModelSerializer):
    file_set = SampleNamedBase64FileSerializer(many=True)

    class Meta:
        model = SampleParentModel
        fields = (
            'id',
            'file_set',
        )
