from rest_framework.test import APITransactionTestCase
from pss_project.api.tests.factories.rest.OLTPBenchRestFactory import OLTPBenchRestFactory
from pss_project.api.tests.utils.utils import generate_dict_factory


class OLTPBenchViewTest(APITransactionTestCase):

    url = '/performance-results/oltpbench/'

    def test_201_response(self):
        """
        Ensure that a valid request sends back a 201
        """
        ClassDictFactory = generate_dict_factory(OLTPBenchRestFactory)
        input = ClassDictFactory()
        response = self.client.post(self.url, data=input, format='json')
        self.assertEqual(response.status_code, 201)

    def test_400_bad_request(self):
        """
        Ensure that an invalid request sends back a 400
        """
        response = self.client.post(self.url, data={'noneya': 'business'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_data_num_validation_rules(self):
        """
        Ensure that an invalid request sends back a 400
        """
        response = self.client.post(self.url, data={'noneya': 'business'}, format='json')
        self.assertContains(response, 'required', count=5, status_code=400)
