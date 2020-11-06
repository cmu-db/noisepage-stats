from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.BinaryMetricsResult import BinaryMetricsResult


class BinaryMetricsResultSerializer(ModelSerializer):
    class Meta:
        model = BinaryMetricsResult
        fields = ('time', 'jenkins_job_id', 'git_branch', 'git_commit_id',
                  'db_version', 'environment', 'metrics')
