from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.ArtifactStatsResult import ArtifactStatsResult


class ArtifactStatsResultSerializer(ModelSerializer):
    class Meta:
        model = ArtifactStatsResult
        fields = ('time', 'jenkins_job_id', 'git_branch', 'git_commit_id',
                  'db_version', 'environment', 'metrics')

    def smudge_timestamp(self):
        while ArtifactStatsResult.objects.filter(time=self.initial_data['time']).count() > 0:
            self.initial_data['time'] = self.initial_data['time'] + timedelta(milliseconds=1)
