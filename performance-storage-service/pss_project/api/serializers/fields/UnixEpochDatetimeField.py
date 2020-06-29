from datetime import datetime
from time import mktime
from rest_framework.serializers import DateTimeField, ValidationError

class UnixEpochDateTimeField(DateTimeField):
    def to_representation(self, value):
        """ Return epoch time for a datetime object or ``None``"""
        try:
            return int(mktime(value.timetuple())*1e3 + value.microsecond/1e3)
        except (AttributeError, TypeError):
            return None

    def to_internal_value(self, value):
        return datetime.fromtimestamp(float(value/1000.0))