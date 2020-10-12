from rest_framework.serializers import Serializer, ChoiceField, DecimalField, IntegerField
from pss_project.api.models.rest.metrics.MicrobenchmarkMetrics import MicrobenchmarkMetrics
from pss_project.api.constants import MICROBENCHMARK_STATUS_CHOICES


class MicrobenchmarkMetricsSerializer(Serializer):
    # Fields
    throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    status = ChoiceField(choices=MICROBENCHMARK_STATUS_CHOICES)
    ref_throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    stdev_throughput = DecimalField(max_digits=24, decimal_places=15, coerce_to_string=False)
    threshold = IntegerField()
    iterations = IntegerField()

    def create(self, validated_data):
        return MicrobenchmarkMetrics(**validated_data)
