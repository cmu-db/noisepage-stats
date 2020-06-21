from django.db import models
from django.contrib.postgres.fields import JSONField

class OLTPBenchResult(models.Model):
    # Constants
    SIMPLE_MODE = 'simple'
    EXTENDED_MODE = 'extended'
    QUERY_MODE_CHOICES = [
        (SIMPLE_MODE,'simple'),
        (EXTENDED_MODE,'extended'),
    ]

    # Fields
    time = models.DateTimeField(auto_now=False)
    branch = models.CharField()
    query_mode = models.CharField(Choices=QUERY_MODE_CHOICES)
    build_id = models.CharField()
    git_commit_id = models.CharField()
    benchmark_type = models.CharField()
    scale_factor = models.DecimalField(max_digits=10,decimal_places=4)
    terminals = models.PositiveSmallIntegerField()
    weights = JSONField()
    metrics = JSONField()
