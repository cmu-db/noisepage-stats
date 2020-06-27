from rest_framework.serializers import Serializer, CharField 
from pss_project.api.serializers.rest.metadata.OLTPBenchMetadataSerializer import OLTPBenchMetadataSerializer
from pss_project.api.serializers.fields.UnixEpochDatetimeField import UnixEpochDateTimeField
from pss_project.api.serializers.rest.parameters.OLTPBenchParametersSerializer import OLTPBenchParametersSerializer
from pss_project.api.serializers.rest.metrics.OLTPBenchMetricsSerializer import OLTPBenchMetricsSerializer
from pss_project.api.models.rest.OLTPBenchRest import OLTPBenchRest

class OLTPBenchSerializer(Serializer):
    # Fields
    metadata = OLTPBenchMetadataSerializer()
    timestamp = UnixEpochDateTimeField()
    type = CharField()
    parameters = OLTPBenchParametersSerializer()
    metrics = OLTPBenchMetricsSerializer()

    def create(self, validated_data):
        return OLTPBenchRest(**validated_data)
