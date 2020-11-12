from rest_framework.serializers import Serializer, DecimalField, IntegerField
from pss_project.api.serializers.rest.metrics.LatencyMetricsSerializer \
    import LatencyMetricsSerializer
from pss_project.api.models.rest.metrics.IncrementalMetrics \
    import IncrementalMetrics


class IncrementalMetricsSerializer(Serializer):
    # Fields
    time = IntegerField()
    throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    latency = LatencyMetricsSerializer(required=False)

    def create(self, validated_data):
        return IncrementalMetrics(**validated_data)
