from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.ArtifactStatsResult import ArtifactStatsResult


class ArtifactStatsResultSerializer(ModelSerializer):
    class Meta:
        model = ArtifactStatsResult
        fields = ('time', 'jenkins_job_id', 'git_branch', 'git_commit_id',
                  'db_version', 'environment', 'metrics')
