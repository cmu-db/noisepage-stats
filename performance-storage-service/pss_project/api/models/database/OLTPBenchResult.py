from django.db.models import Model, DateTimeField, CharField, DecimalField, PositiveSmallIntegerField
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder


class OLTPBenchResult(Model):
    class Meta:
        db_table = 'oltpbench_results'

    # Constants
    SIMPLE_MODE = 'simple'
    EXTENDED_MODE = 'extended'
    QUERY_MODE_CHOICES = [
        (SIMPLE_MODE, 'simple'),
        (EXTENDED_MODE, 'extended'),
    ]
    RAM_DISK = 'RAM disk'
    HDD = 'HDD'
    SATA_SSD = 'SATA SSD'
    NVME_SSD = 'NVMe SSD'
    WAL_DEVICE_CHOICES = [
        (RAM_DISK, 'RAM disk'),
        (HDD, 'HDD'),
        (SATA_SSD, 'SATA SSD'),
        (NVME_SSD, 'NVMe SSD')
    ]

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
    weights = JSONField()
    wal_device = CharField(max_length=30, choices=WAL_DEVICE_CHOICES)
    max_connection_threads = PositiveSmallIntegerField()
    metrics = JSONField(encoder=DjangoJSONEncoder)
    incremental_metrics = JSONField(encoder=DjangoJSONEncoder)
