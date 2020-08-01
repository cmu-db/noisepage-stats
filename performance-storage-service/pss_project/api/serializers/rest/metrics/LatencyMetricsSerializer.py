from rest_framework.serializers import Serializer, DecimalField
from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics


class LatencyMetricsSerializer(Serializer):
    l_25 = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    l_75 = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    l_90 = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    l_95 = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    l_99 = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    avg = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    median = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    max = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    min = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)

    def create(self, validated_data):
        return LatencyMetrics(**validated_data)
