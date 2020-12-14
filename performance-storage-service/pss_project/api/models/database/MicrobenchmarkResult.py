from django.db.models import (Model, DateTimeField, CharField, PositiveSmallIntegerField, PositiveIntegerField,
                              JSONField)
from django.core.serializers.json import DjangoJSONEncoder
from pss_project.api.constants import WAL_DEVICE_CHOICES


class MicrobenchmarkResult(Model):
    """ This class is the model for storing microbenchmark test results in the database. For more information about the
    schema check out the wiki: 
    https://github.com/cmu-db/noisepage-stats/wiki/Timescaledb-Schema#microbenchmark_results-table """

    class Meta:
        db_table = 'microbenchmark_results'

    time = DateTimeField(auto_now=False)
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
