from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.MicrobenchmarkResult import MicrobenchmarkResult


class MicrobenchmarkResultSerializer(ModelSerializer):
    class Meta:
        model = MicrobenchmarkResult
        fields = ('time', 'jenkins_job_id', 'git_branch', 'git_commit_id',
                  'db_version', 'environment', 'benchmark_suite', 'benchmark_name',
                  'threads', 'min_runtime', 'wal_device', 'metrics')

    def smudge_timestamp(self):
        while MicrobenchmarkResult.objects.filter(time=self.initial_data['time']).count() > 0:
            self.initial_data['time'] = self.initial_data['time'] + timedelta(milliseconds=1)
