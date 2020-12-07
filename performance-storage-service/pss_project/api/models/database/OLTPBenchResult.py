from datetime import datetime, timedelta
from django.utils import timezone

from django.db.models import Model, DateTimeField, CharField, DecimalField, PositiveSmallIntegerField, JSONField
from django.core.serializers.json import DjangoJSONEncoder
from pss_project.api.constants import QUERY_MODE_CHOICES, WAL_DEVICE_CHOICES

PERFORMANCE_CONFIG_FIELDS = ['query_mode', 'benchmark_type', 'scale_factor', 'terminals', 'client_time', 'weights',
                             'wal_device', 'max_connection_threads']


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

    def get_test_config(self):
        """ Return a dict with the fields related to the OLTPBench test config """
        config = {}
        for field in PERFORMANCE_CONFIG_FIELDS:
            config[field] = getattr(self, field)
        return config

    def get_oltpbench_config_query(self, branch):
        """ Returns a query set for a branch based on the current object's config. This is used to create a query to
        compare similar test results across branches. """
        filters = {
            "git_branch": branch,
            "time__gte": datetime.now(timezone.utc)-timedelta(days=7),
        }
        for field in PERFORMANCE_CONFIG_FIELDS:
            filters[field] = getattr(self, field)
        return OLTPBenchResult.objects.filter(**filters)

    def is_config_match(self, oltpbench_result):
        """ Checks whether another OLTPBenchResult object has a matching config to the current object. """
        for field in PERFORMANCE_CONFIG_FIELDS:
            if getattr(self, field) != getattr(oltpbench_result, field):
                return False
        return True

    def compare_throughput(self, oltpbench_result):
        """ Calculate the % difference between the current OLTPBenchResult object and another OLTPBenchResult object.
        If the field name changes this will just return that there was no change.
        """
        config = {}
        for field in PERFORMANCE_CONFIG_FIELDS:
            config[field] = getattr(self, field)
        base_throughput = float(self.metrics.get('throughput', 0))
        if base_throughput == 0:
            return 0
        new_throughput = float(oltpbench_result.metrics.get('throughput', 0))
        percent_diff = (new_throughput - base_throughput) / base_throughput * 100
        return percent_diff

    @classmethod
    def get_all_branch_results(cls, branch):
        """ Return a query set that will return all results for a given branch. """
        branch_results = cls.objects.filter(git_branch=branch)
        return branch_results

    @classmethod
    def get_latest_branch_results(cls, branch):
        """ Return a query set that will return all the latest OLTPBenchResults for each unique test config in a given
        branch. """
        branch_results = cls.objects.filter(git_branch=branch, time__gte=datetime.now(
            timezone.utc)-timedelta(days=7)).order_by(*PERFORMANCE_CONFIG_FIELDS+['time']).reverse()
        return branch_results.distinct(*PERFORMANCE_CONFIG_FIELDS)

    @classmethod
    def get_branch_results_by_oltpbench_configs(cls, branch, oltpbench_results):
        """ Return a query set of the latest OLTPBenchResults in a branch for each OLTPBench config passed in
        the oltpbench_results array. """
        master_results_query = cls.objects.none()
        for config in oltpbench_results:
            master_results_query = master_results_query | config.get_oltpbench_config_query(branch)
        return master_results_query.order_by(*PERFORMANCE_CONFIG_FIELDS+['time']) \
            .reverse().distinct(*PERFORMANCE_CONFIG_FIELDS)
