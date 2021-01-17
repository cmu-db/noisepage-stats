from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult


class OLTPBenchResultSerializer(ModelSerializer):
    class Meta:
        model = OLTPBenchResult
        fields = ('time', 'git_branch', 'git_commit_id', 'jenkins_job_id', 'db_version', 'environment',
                  'benchmark_type', 'query_mode', 'scale_factor', 'terminals', 'client_time', 'weights',
                  'wal_device', 'max_connection_threads', 'metrics', 'incremental_metrics')

    def smudge_timestamp(self):
        while OLTPBenchResult.objects.filter(time=self.initial_data['time']).count() > 0:
            self.initial_data['time'] = self.initial_data['time'] + timedelta(milliseconds=1)