from rest_framework.test import APITransactionTestCase
from pss_project.api.tests.factories.rest.OLTPBenchRestFactory import OLTPBenchRestFactory
from pss_project.api.tests.utils.utils import generate_dict_factory
from pss_project.api.tests.utils.utils import get_basic_auth_header
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class OLTPBenchViewTest(APITransactionTestCase):

    test_username = 'testuser'
    test_password = 'password'

    def setUp(self):
        self.url = '/performance-results/oltpbench/'
        self.client = APIClient()

        test_user = User.objects.create_user(
            username=self.test_username, password=self.test_password)
        test_user.save()
        self.credentials = get_basic_auth_header(
            self.test_username, self.test_password)

    def test_403_forbidden_error(self):
        """
        Ensure that an invalid request sends back a 403
        """
        # unset any existing credentials
        self.client.credentials()
        response = self.client.post(
            self.url, data={'noneya': 'business'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_201_response(self):
        """
        Ensure that a valid request sends back a 201
        """
        ClassDictFactory = generate_dict_factory(OLTPBenchRestFactory)
        input = ClassDictFactory()
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)
        response = self.client.post(self.url, data=input, format='json')
        self.assertEqual(response.status_code, 201)

    def test_201_response_smudge_time(self):
        """
        Ensure that a second request with the time is saved appropriately
        """
        ClassDictFactory = generate_dict_factory(OLTPBenchRestFactory)
        input = ClassDictFactory()
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)
        self.client.post(self.url, data=input, format='json')
        response = self.client.post(self.url, data=input, format='json')
        self.assertEqual(response.status_code, 201)

    def test_400_bad_request(self):
        """
        Ensure that an invalid request sends back a 400
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)
        response = self.client.post(
            self.url, data={'noneya': 'business'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_data_num_validation_rules(self):
        """
        Ensure that an invalid request sends back a 400
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)
        response = self.client.post(
            self.url, data={'noneya': 'business'}, format='json')
        self.assertContains(response, 'required', count=5, status_code=400)
