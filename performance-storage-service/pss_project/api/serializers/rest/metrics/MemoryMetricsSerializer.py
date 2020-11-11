from rest_framework.serializers import Serializer, DecimalField
from pss_project.api.models.rest.metrics.MemoryMetrics import MemoryMetrics, MemoryItemSummary


class MemoryItemSummarySerializer(Serializer):
    avg = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)

    def create(self, validated_data):
        return MemoryItemSummarySerializer(**validated_data)


class MemoryMetricsSerializer(Serializer):
    rss = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    vms = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)

    def create(self, validated_data):
        return MemoryMetrics(**validated_data)


class MemorySummaryMetricsSerializer(Serializer):
    rss = MemoryItemSummarySerializer(required=False)
    vms = MemoryItemSummarySerializer(required=False)

    def create(self, validated_data):
        return MemoryMetrics(**validated_data)