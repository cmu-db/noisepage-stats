from django.test import SimpleTestCase
from datetime import datetime

from pss_project.api.serializers.fields.UnixEpochDatetimeField import UnixEpochDateTimeField

class TestUnixEpochDateTimeField(SimpleTestCase):
    def setUp(self):
        self.field = UnixEpochDateTimeField()

    def test_to_representation(self):
        """ Convert datetime to timestamp"""
        input = datetime.now().replace(microsecond=0)
        result = self.field.to_representation(input)
        self.assertEqual(datetime.fromtimestamp(float(result/1000.0)), input)

    def test_to_internal_value(self):
        """ Convert timestamp to datetime """
        input = datetime.now().timestamp()
        result = self.field.to_internal_value(input)
        self.assertEqual(result, datetime.fromtimestamp(float(input/1000.0)))