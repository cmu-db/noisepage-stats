from datetime import timedelta
from django.db.models import (Model, DateTimeField, CharField, PositiveSmallIntegerField, PositiveIntegerField,
                              JSONField)
from django.db import IntegrityError
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateparse import parse_datetime
from pss_project.api.constants import WAL_DEVICE_CHOICES


class MicrobenchmarkResult(Model):
    """ This class is the model for storing microbenchmark test results in the database. For more information about the
    schema check out the wiki:
    https://github.com/cmu-db/noisepage-stats/wiki/Timescaledb-Schema#microbenchmark_results-table """

    class Meta:
        db_table = 'microbenchmark_results'

    time = DateTimeField(primary_key=True, auto_now=False, validators=[])
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

    def save(self, *args, **kwargs):
        self.save_and_smear_timestamp(*args, **kwargs)

    def save_and_smear_timestamp(self, *args, **kwargs):
        """Recursivly try to save by incrementing the timestamp on duplicate error"""
        try:
            super().save(*args, **kwargs)
        except IntegrityError as exception:
            # Only handle the error:
            #   psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint
            #   "1_1_farms_sensorreading_pkey"
            #   DETAIL:  Key ("time")=(2020-10-01 22:33:52.507782+00) already exists.
            if all(k in exception.args[0] for k in ("Key", "time", "already exists")):
                # Increment the timestamp by 1 ms and try again
                self.time = str(parse_datetime(self.time) + timedelta(milliseconds=1))
                self.save_and_smear_timestamp(*args, **kwargs)
