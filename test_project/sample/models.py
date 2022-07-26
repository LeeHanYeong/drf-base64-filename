from django.db import models


class SampleParentModel(models.Model):
    pass


class SampleBase64ImageModel(models.Model):
    parent = models.ForeignKey(
        SampleParentModel,
        on_delete=models.CASCADE,
        related_name="image_set",
        blank=True,
        null=True,
    )
    image = models.ImageField(blank=True)


class SampleBase64FileModel(models.Model):
    parent = models.ForeignKey(
        SampleParentModel,
        on_delete=models.CASCADE,
        related_name="file_set",
        blank=True,
        null=True,
    )
    file = models.FileField(blank=True)
