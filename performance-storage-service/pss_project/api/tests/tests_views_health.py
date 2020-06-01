from rest_framework.test import APITestCase
from django.urls import reverse

# Create your tests here.
class HealthViewTest(APITestCase):
    url = '/health/'
    def test_200_response(self):
        """
        Ensure the health endpoint sends back a 200
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uptime_exists(self):
        """
        Ensure the health endpoint sends back uptime
        """
        response = self.client.get(self.url)
        self.assertTrue('uptime' in response.data)
