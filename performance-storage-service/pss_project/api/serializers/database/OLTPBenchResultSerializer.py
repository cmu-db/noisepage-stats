from rest_framework.serializers import ModelSerializer, Serializer, Field, DateTimeField, SerializerMethodField, CharField
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult
from pss_project.api.serializers.fields.UnixEpochDatetimeField import UnixEpochDateTimeField


class OLTPBenchResultSerializer(ModelSerializer):
    class Meta:
        model = OLTPBenchResult
        fields = ('time', 'branch', 'query_mode', 'build_id', 'git_commit_id',
                  'benchmark_type', 'scale_factor', 'terminals', 'duration', 'weights', 'metrics')
