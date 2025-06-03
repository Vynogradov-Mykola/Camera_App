from django.test import TestCase, Client
from django.urls import reverse
from cameras.models import Camera


class CameraViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.camera = Camera.objects.create(name="Test Cam", location="Lab 1")

    def test_camera_list_view(self):
        response = self.client.get(reverse('camera_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cameras/camera_list.html')
        self.assertContains(response, "Test Cam")

    def test_camera_stream_view(self):
        response = self.client.get(reverse('camera_stream'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cameras/camera_stream.html')
