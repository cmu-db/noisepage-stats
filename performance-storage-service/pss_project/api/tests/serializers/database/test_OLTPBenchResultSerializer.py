from django.test import TestCase
from django.utils.dateparse import parse_datetime

from pss_project.api.tests.factories.database.OLTPBenchDBFactory import OLTPBenchDBFactory
from pss_project.api.tests.factories.rest.OLTPBenchRestFactory import OLTPBenchRestFactory
from pss_project.api.serializers.database.OLTPBenchResultSerializer import OLTPBenchResultSerializer


class TestOLTPBenchResultSerializer(TestCase):

    def test_serialize_model_fields(self):
        """ Assert """
        input = OLTPBenchDBFactory()
        serializer = OLTPBenchResultSerializer(instance=input)
        for key in serializer.data.keys():
            input_value = getattr(input, key)
            if isinstance(input_value, float):
                self.assertEqual(float(serializer.data[key]), input_value)
            else:
                self.assertEqual(serializer.data[key], input_value)

    def test_deserialize_model_fields(self):
        factory = OLTPBenchRestFactory()
        input = factory.convert_to_db_json()
        serializer = OLTPBenchResultSerializer(data=input)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    def test_smudge_timestamp(self):
        existing_db_entry = OLTPBenchDBFactory()
        existing_db_entry.save()
        factory = OLTPBenchRestFactory()
        factory.timestamp = parse_datetime(existing_db_entry.time)
        input = factory.convert_to_db_json()
        serializer = OLTPBenchResultSerializer(data=input)
        serializer.smudge_timestamp()
        self.assertNotEqual(serializer.initial_data['time'],parse_datetime(existing_db_entry.time))
