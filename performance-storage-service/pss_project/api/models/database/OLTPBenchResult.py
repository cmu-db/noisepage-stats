from django.db.models import Model, DateTimeField, CharField, DecimalField, PositiveSmallIntegerField, JSONField
from django.core.serializers.json import DjangoJSONEncoder
from pss_project.api.constants import QUERY_MODE_CHOICES, WAL_DEVICE_CHOICES


class OLTPBenchResult(Model):
    class Meta:
        db_table = 'oltpbench_results'

    # Fields
    time = DateTimeField(auto_now=False)
    query_mode = CharField(max_length=30, choices=QUERY_MODE_CHOICES)
    jenkins_job_id = CharField(max_length=15)
    git_branch = CharField(max_length=255)
    git_commit_id = CharField(max_length=40)
    db_version = CharField(max_length=255)
    environment = JSONField()
    benchmark_type = CharField(max_length=20)
    scale_factor = DecimalField(max_digits=10, decimal_places=4)
    terminals = PositiveSmallIntegerField()
    client_time = PositiveSmallIntegerField()
    weights = JSONField(encoder=DjangoJSONEncoder)
    wal_device = CharField(max_length=30, choices=WAL_DEVICE_CHOICES)
    max_connection_threads = PositiveSmallIntegerField()
    metrics = JSONField(encoder=DjangoJSONEncoder)
    incremental_metrics = JSONField(encoder=DjangoJSONEncoder)
