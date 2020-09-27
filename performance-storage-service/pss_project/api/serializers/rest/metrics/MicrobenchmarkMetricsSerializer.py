from rest_framework.serializers import Serializer, RegexField, DecimalField, IntegerField
from pss_project.api.models.rest.metrics.MicrobenchmarkMetrics import MicrobenchmarkMetrics


class MicrobenchmarkMetricsSerializer(Serializer):
    # Fields
    throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    name = RegexField(regex=r'^[^/]+/[^/]+$')
    iterations = IntegerField(required=False)
    real_time = IntegerField(required=False)
    cpu_time = IntegerField(required=False)
    bytes_per_second = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)

    def create(self, validated_data):
        return MicrobenchmarkMetrics(**validated_data)
