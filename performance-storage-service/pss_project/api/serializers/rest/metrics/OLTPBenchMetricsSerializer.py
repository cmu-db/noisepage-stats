from rest_framework.serializers import Serializer, DecimalField, JSONField
from pss_project.api.serializers.rest.metrics.LatencyMetricsSerializer import LatencyMetricsSerializer
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics

class OLTPBenchMetricsSerializer(Serializer):
    # Fields
    throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    latency = LatencyMetricsSerializer(required=False)
    incremental_metrics = JSONField()

    def create(self, validated_data):
        return OLTPBenchMetrics(**validated_data)