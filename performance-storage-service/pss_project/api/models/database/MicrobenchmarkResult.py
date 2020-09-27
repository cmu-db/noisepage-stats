from django.db.models import Model, DateTimeField, CharField, PositiveSmallIntegerField, PositiveIntegerField
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from pss_project.api.constants import QUERY_MODE_CHOICES, WAL_DEVICE_CHOICES


class MicrobenchmarkResult(Model):
    class Meta:
        db_table = 'microbenchmark_results'

    time = DateTimeField(auto_now=False)
    query_mode = CharField(max_length=30, choices=QUERY_MODE_CHOICES)
    jenkins_job_id = CharField(max_length=15)
    git_branch = CharField(max_length=255)
    git_commit_id = CharField(max_length=40)
    db_version = CharField(max_length=255)
    environment = JSONField()
    benchmark_suite = CharField(max_length=255)
    benchmark_name = CharField(max_length=255)
    threads = PositiveSmallIntegerField()
    min_runtime = PositiveIntegerField()
    wal_device = CharField(max_length=30, choices=WAL_DEVICE_CHOICES)
    metrics = JSONField(encoder=DjangoJSONEncoder)
