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

    # Fields
    time = DateTimeField(auto_now=False)
    branch = CharField(max_length=255)
    query_mode = CharField(max_length=30, choices=QUERY_MODE_CHOICES)
    build_id = CharField(max_length=15)
    git_commit_id = CharField(max_length=40)
    benchmark_type = CharField(max_length=20)
    scale_factor = DecimalField(max_digits=10, decimal_places=4)
    terminals = PositiveSmallIntegerField()
    duration = PositiveSmallIntegerField()
    weights = JSONField()
    metrics = JSONField(encoder=DjangoJSONEncoder)
