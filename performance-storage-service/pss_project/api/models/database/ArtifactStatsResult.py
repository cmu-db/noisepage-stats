from django.db.models import Model, DateTimeField, CharField, JSONField
from django.core.serializers.json import DjangoJSONEncoder


class ArtifactStatsResult(Model):
    """ This class is the model for storing artifact stats results in the database. For more information about the
    schema check out the wiki:
    https://github.com/cmu-db/noisepage-stats/wiki/Timescaledb-Schema#artifact_stats_results-table """

    class Meta:
        db_table = 'artifact_stats_results'

    time = DateTimeField(primary_key=True, auto_now=False)
    jenkins_job_id = CharField(max_length=15)
    git_branch = CharField(max_length=255)
    git_commit_id = CharField(max_length=40)
    db_version = CharField(max_length=255)
    environment = JSONField()
    metrics = JSONField(encoder=DjangoJSONEncoder)
