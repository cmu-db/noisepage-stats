from django.test import TestCase

from pss_project.api.tests.factories.database.BinaryMetricsDBFactory import BinaryMetricsDBFactory
from pss_project.api.tests.factories.rest.BinaryMetricsRestFactory import BinaryMetricsRestFactory
from pss_project.api.serializers.database.BinaryMetricsResultSerializer import BinaryMetricsResultSerializer


class TestMicrobenchmarkResultSerializer(TestCase):
    def test_serialize_model_fields(self):
        input = BinaryMetricsDBFactory()
        serializer = BinaryMetricsResultSerializer(instance=input)
        for key in serializer.data.keys():
            input_value = getattr(input, key)
            if isinstance(input_value, float):
                self.assertEqual(float(serializer.data[key]), input_value)
            else:
                self.assertEqual(serializer.data[key], input_value)

    def test_deserializer_model_fields(self):
        factory = BinaryMetricsRestFactory()
        input = factory.convert_to_db_json()
        serializer = BinaryMetricsResultSerializer(data=input)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
