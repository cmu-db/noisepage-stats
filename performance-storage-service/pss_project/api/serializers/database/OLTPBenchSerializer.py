from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult

class OLTPBenchSerializer(ModelSerializer):
    class Meta:
        model = OLTPBenchResult
        fields = ['time','branch','query_mode','build_id','git_commit_id',
            'benchmark_type','scale_factor','terminals','duration','weights','metrics']