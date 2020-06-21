from rest_framework.serializers import Serializer, DecimalField, IntegerField
from pss_project.api.serializers.rest.parameters.TransactionWeightSerializer import TransactionWeightSerializer
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics

class OLTPBenchMetricsSerializer(Serializer):
    # Fields
    throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    latency_99 = IntegerField(required=False)
    latency_95 = IntegerField(required=False)
    latency_avg = IntegerField(required=False)
    latency_max = IntegerField(required=False)

    def create(self, validated_data):
        return OLTPBenchMetrics(**validated_data)