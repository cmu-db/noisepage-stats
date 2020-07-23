from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult


class OLTPBenchResultSerializer(ModelSerializer):
    class Meta:
        model = OLTPBenchResult
        fields = ('time', 'git_branch', 'git_commit_id', 'jenkins_job_id', 'db_version', 'environment',
                  'benchmark_type', 'query_mode', 'scale_factor', 'terminals', 'client_time', 'weights',
                  'metrics', 'incremental_metrics')
