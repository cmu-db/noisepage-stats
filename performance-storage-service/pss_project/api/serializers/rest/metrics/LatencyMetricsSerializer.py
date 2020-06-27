from rest_framework.serializers import Serializer, IntegerField
from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics

class LatencyMetricsSerializer(Serializer):
    l_25 = IntegerField(required=False)
    l_75 = IntegerField(required=False)
    l_90 = IntegerField(required=False)
    l_95 = IntegerField(required=False)
    l_99 = IntegerField(required=False) 
    avg = IntegerField(required=False)
    median = IntegerField(required=False)
    max = IntegerField(required=False)
    min = IntegerField(required=False)

    def create(self, validated_data):
        return LatencyMetrics(**validated_data)