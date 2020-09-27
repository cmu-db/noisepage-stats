from django.test import TestCase

from pss_project.api.tests.factories.database.MicrobenchmarkDBFactory import MicrobenchmarkDBFactory
from pss_project.api.tests.factories.rest.MicrobenchmarkRestFactory import MicrobenchmarkRestFactory
from pss_project.api.serializers.database.MicrobenchmarkResultSerializer import MicrobenchmarkResultSerializer


class TestMicrobenchmarkResultSerializer(TestCase):
    def test_serialize_model_fields(self):
        input = MicrobenchmarkDBFactory()
        serializer = MicrobenchmarkResultSerializer(instance=input)
        for key in serializer.data.keys():
            input_value = getattr(input, key)
            if isinstance(input_value, float):
                self.assertEqual(float(serializer.data[key]), input_value)
            else:
                self.assertEqual(serializer.data[key], input_value)

    def test_deserializer_model_fields(self):
        factory = MicrobenchmarkRestFactory()
        input = factory.convert_to_arr_db_json()[0]
        serializer = MicrobenchmarkResultSerializer(data=input)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
