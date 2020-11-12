from django.test import TestCase

from pss_project.api.tests.factories.database.ArtifactStatsDBFactory import ArtifactStatsDBFactory
from pss_project.api.tests.factories.rest.ArtifactStatsRestFactory import ArtifactStatsRestFactory
from pss_project.api.serializers.database.ArtifactStatsResultSerializer import ArtifactStatsResultSerializer


class TestMicrobenchmarkResultSerializer(TestCase):
    def test_serialize_model_fields(self):
        input = ArtifactStatsDBFactory()
        serializer = ArtifactStatsResultSerializer(instance=input)
        for key in serializer.data.keys():
            input_value = getattr(input, key)
            if isinstance(input_value, float):
                self.assertEqual(float(serializer.data[key]), input_value)
            else:
                self.assertEqual(serializer.data[key], input_value)

    def test_deserializer_model_fields(self):
        factory = ArtifactStatsRestFactory()
        input = factory.convert_to_db_json()
        serializer = ArtifactStatsResultSerializer(data=input)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)