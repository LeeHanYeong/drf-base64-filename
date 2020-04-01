import base64
import filecmp
import os
from copy import deepcopy

from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SampleBase64ImageModel, SampleParentModel

PATH_IMAGE = finders.find(os.path.join('drf_base64', 'image', 'sample_jpg.jpg'))
PATH_BASE64_STR = finders.find(os.path.join('drf_base64', 'image', 'sample_jpg.txt'))
PATH_IMAGE_PNG = finders.find(os.path.join('drf_base64', 'image', 'sample_png.png'))
PATH_BASE64_STR_PNG = finders.find(os.path.join('drf_base64', 'image', 'sample_png.txt'))

URL_IMAGE = '/image/'
URL_FILE = '/file/'
URL_FILENAME_IMAGE = '/image-name/'
URL_FILENAME_FILE = '/file-name/'
URL_PARENT_IMAGE = '/parent-image-name/'


def _create_image_instance(**kwargs):
    file = SimpleUploadedFile(os.path.basename(PATH_IMAGE), open(PATH_IMAGE, 'rb').read())
    return baker.make(SampleBase64ImageModel, image=file, **kwargs)


class Base64ImageConvertTest(TestCase):
    def test_encode(self):
        content = open(PATH_IMAGE, 'rb').read()
        encoded_str = base64.b64encode(content).decode('utf-8')

        self.assertEqual(
            encoded_str, open(PATH_BASE64_STR, 'rt').read()
        )

    def test_decode(self):
        content = open(PATH_BASE64_STR, 'rb').read()
        decoded_str = base64.decodebytes(content)

        self.assertEqual(
            decoded_str, open(PATH_IMAGE, 'rb').read()
        )


class Base64ImageAPITest(APITestCase):
    URL = URL_IMAGE

    def test_create(self):
        base64_str = open(PATH_BASE64_STR, 'rt').read()
        response = self.client.post(self.URL, {'image': base64_str})
        self.assertIsNotNone(response.data['image'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 1)
        instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))


class WithFilenameCreateAPITest(APITestCase):
    URL = URL_FILENAME_IMAGE

    def test_create(self):
        base64_str = open(PATH_BASE64_STR, 'rt').read()
        data = {
            'image': {
                'file_name': 'pby.jpg',
                'encoded_str': base64_str,
            }
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertIsNotNone(response.data['image'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 1)
        instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))
        self.assertTrue('pby' in instance.image.name)

    def test_create_blank_null(self):
        data1 = {'image': None}
        data2 = {'image': ''}
        for data in (data1, data2):
            response = self.client.post(self.URL, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIsNone(response.data['image'])

            instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
            self.assertFalse(instance.image)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 2)


class WithFilenameUpdateAPITest(APITestCase):
    URL = URL_FILENAME_IMAGE

    def test_update(self):
        base64_str_png = open(PATH_BASE64_STR_PNG, 'rt').read()
        instance = _create_image_instance()
        self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))

        # Retrieve/Update URL
        url = self.URL + f'{instance.pk}/'

        retrieve_response = self.client.get(url)
        retrieve_data = retrieve_response.data
        data = {
            **retrieve_data,
            'image': {
                'file_name': 'weepinmie.png',
                'encoded_str': base64_str_png,
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
        self.assertTrue(filecmp.cmp(updated_instance.image.path, PATH_IMAGE_PNG))

    def test_update_blank_null(self):
        for value in (None, ''):
            instance = _create_image_instance()
            self.assertTrue(filecmp.cmp(instance.image.path, PATH_IMAGE))

            # Retrieve/Update URL
            url = self.URL + f'{instance.pk}/'

            retrieve_response = self.client.get(url)
            retrieve_data = retrieve_response.data

            data = {**retrieve_data, 'image': value}
            response = self.client.patch(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertIsNone(response.data['image'])
            updated_instance = SampleBase64ImageModel.objects.get(id=response.data['id'])
            self.assertFalse(updated_instance.image)

    def test_update_ignore_url(self):
        """
        When an update is requested using the response data received by list or retrieve,
        Pass validation and verify that the field's value does not change
        """
        instance = _create_image_instance()

        # Retrieve/Update URL
        url = self.URL + f'{instance.pk}/'

        retrieve_response = self.client.get(url)
        retrieve_data = retrieve_response.data
        retrieve_url = retrieve_data['image']

        update_response = self.client.patch(url, retrieve_data, format='json')
        update_data = update_response.data
        update_url = update_data['image']
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_url, update_url)


class WithFilenameWritableNestedAPITest(APITestCase):
    URL = URL_PARENT_IMAGE

    def test_create(self):
        data = {
            'image_set': [
                {
                    'image': {
                        'file_name': 'sample_jpg.jpg',
                        'encoded_str': open(PATH_BASE64_STR, 'rt').read(),
                    },
                },
                {
                    'image': {
                        'file_name': 'sample_png.png',
                        'encoded_str': open(PATH_BASE64_STR_PNG, 'rt').read(),
                    }
                },
            ],
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        parent = baker.make(SampleParentModel)
        image_set = _create_image_instance(parent=parent, _quantity=2)

        url = self.URL + f'{parent.pk}/'
        response = self.client.get(url)
        origin_data = response.data
        self.assertTrue(filecmp.cmp(*[image.image.path for image in image_set]))

        origin_image_data_1 = origin_data['image_set'][0]
        origin_image_data_2 = origin_data['image_set'][1]
        origin_image_1 = SampleBase64ImageModel.objects.get(id=origin_image_data_1['id'])
        origin_image_2 = SampleBase64ImageModel.objects.get(id=origin_image_data_2['id'])

        data = deepcopy(origin_data)
        data['image_set'][1] = {
            'image': {
                'file_name': 'sample_png.png',
                'encoded_str': open(PATH_BASE64_STR_PNG, 'rt').read(),
            }
        }
        update_response = self.client.patch(url, data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        update_data = update_response.data
        self.assertEqual(len(update_data['image_set']), 2)
        self.assertEqual(SampleBase64ImageModel.objects.count(), 2)

        # 2번째 이미지의 파일이 update시 주어진 파일과 같은지 검사
        image_data_1 = update_data['image_set'][0]
        image_data_2 = update_data['image_set'][1]
        image_1 = SampleBase64ImageModel.objects.get(id=image_data_1['id'])
        image_2 = SampleBase64ImageModel.objects.get(id=image_data_2['id'])
        self.assertTrue(filecmp.cmp(image_1.image.path, PATH_IMAGE))
        self.assertTrue(filecmp.cmp(image_2.image.path, PATH_IMAGE_PNG))

        # 1번째 이미지는 같으며, update된 2번째 이미지는 다름을 확인
        self.assertEqual(origin_image_1, image_1)
        self.assertNotEqual(origin_image_2, image_2)

        # Update시 제외된 항목의 삭제 확인
        self.assertFalse(SampleBase64ImageModel.objects.filter(id=origin_image_data_2['id']))

    def test_update_no_change(self):
        parent = baker.make(SampleParentModel)
        image_set = _create_image_instance(parent=parent, _quantity=2)

        url = self.URL + f'{parent.pk}/'
        response = self.client.get(url)
        origin_data = response.data
        self.assertTrue(filecmp.cmp(*[image.image.path for image in image_set]))

        update_response = self.client.patch(url, origin_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        update_data = update_response.data
        self.assertDictEqual(origin_data, update_data)
