# drf-base64-filename

**drf-base64-filename** provides Serializer fields for using base64-encoded files with file names.

## Setup

Install `drf-base64-filename` to your Python environment

```shell
pip install drf-base64-filename
```



## Usage

### Sample Model

```python
class SampleBase64ImageModel(models.Model):
    parent = models.ForeignKey(
        SampleParentModel, 
        on_delete=models.CASCADE, 
        related_name='image_set', 
        blank=True, 
        null=True,
    )
    image = models.ImageField(blank=True)

class SampleBase64FileModel(models.Model):
    parent = models.ForeignKey(
        SampleParentModel, 
        on_delete=models.CASCADE,
        related_name='file_set', 
        blank=True, 
        null=True,
    )
    file = models.FileField(blank=True)
```



### Serializer Field

```python
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
```



### Sample request data

```json
{
    "image": {
        "file_name": "pby.jpg",
        "encoded_str": "aHR0cHM6Ly9naXRodWIuY29tL2xlZWhhbnllb25n"
    }
}
```

### Sample response data

```json
{
    "image": "http://test/media/pby.jpg"
}
```



# Testing

```shell
cd test_project
pip install -r requirements.txt
pytest
```



## Contributing

As an open source project, we welcome contributions.
The code lives on [GitHub](https://github.com/LeeHanYeong/drf-base64-filename)

 