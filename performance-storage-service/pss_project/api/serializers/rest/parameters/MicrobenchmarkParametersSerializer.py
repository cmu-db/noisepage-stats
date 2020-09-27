from rest_framework.serializers import Serializer, ChoiceField, IntegerField
from pss_project.api.models.rest.parameters.MicrobenchmarkParameters import MicrobenchmarkParameters
from pss_project.api.constants import QUERY_MODE_CHOICES


class MicrobenchmarkParametersSerializer(Serializer):

    # Fields
    query_mode = ChoiceField(choices=QUERY_MODE_CHOICES)
    threads = IntegerField()
    min_runtime = IntegerField()

    def create(self, validated_data):
        return MicrobenchmarkParameters(**validated_data)
