from django.db.models import Model, DateTimeField, CharField
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder


class BinaryMetricsResult(Model):
    class Meta:
        db_table = 'binary_metrics_results'

    time = DateTimeField(auto_now=False)
    jenkins_job_id = CharField(max_length=15)
    git_branch = CharField(max_length=255)
    git_commit_id = CharField(max_length=40)
    db_version = CharField(max_length=255)
    environment = JSONField()
    metrics = JSONField(encoder=DjangoJSONEncoder)
