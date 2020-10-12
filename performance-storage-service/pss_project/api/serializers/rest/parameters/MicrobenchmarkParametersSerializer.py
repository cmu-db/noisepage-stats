from rest_framework.serializers import Serializer, IntegerField
from pss_project.api.models.rest.parameters.MicrobenchmarkParameters import MicrobenchmarkParameters


class MicrobenchmarkParametersSerializer(Serializer):

    # Fields
    threads = IntegerField()
    min_runtime = IntegerField()

    def create(self, validated_data):
        return MicrobenchmarkParameters(**validated_data)
