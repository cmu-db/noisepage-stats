from rest_framework.serializers import Serializer, JSONField
from django.core.serializers.json import DjangoJSONEncoder
from pss_project.api.serializers.rest.metadata.MetadataSerializer import MetadataSerializer
from pss_project.api.serializers.fields.UnixEpochDatetimeField import UnixEpochDateTimeField
from pss_project.api.models.rest.BinaryMetricsRest import BinaryMetricsRest


class BinaryMetricsSerializer(Serializer):
    # Fields
    metadata = MetadataSerializer()
    timestamp = UnixEpochDateTimeField()
    metrics = JSONField(encoder=DjangoJSONEncoder)

    def create(self, validated_data):
        return BinaryMetricsRest(**validated_data)
