from pss_project.api.models.rest.metadata.Metadata import Metadata
from pss_project.api.models.rest.parameters.MicrobenchmarkParameters import MicrobenchmarkParameters
from pss_project.api.models.rest.metrics.MicrobenchmarkMetrics import MicrobenchmarkMetrics
from pss_project.api.models.rest.utils import convert_environment_to_dict


class MicrobenchmarkRest(object):
    def __init__(self, metadata, timestamp, test_suite, test_name, parameters, metrics):
        self.metadata = Metadata(**metadata)
        self.timestamp = timestamp
        self.test_suite = test_suite
        self.test_name = test_name
        self.parameters = MicrobenchmarkParameters(**parameters)
        self.metrics = MicrobenchmarkMetrics(**metrics)

    def convert_to_db_json(self):
        return {
            'time': self.timestamp,
            'jenkins_job_id': self.metadata.jenkins.jenkins_job_id,
            'git_branch': self.metadata.github.git_branch,
            'git_commit_id':  self.metadata.github.git_commit_id,
            'db_version': self.metadata.noisepage.db_version,
            'environment': convert_environment_to_dict(self.metadata.environment),
            'benchmark_suite': self.test_suite,
            'benchmark_name': self.test_name,
            'threads': self.parameters.threads,
            'min_runtime': self.parameters.min_runtime,
            'wal_device': self.metadata.environment.wal_device,
            'metrics': self.metrics.__dict__,
        }
