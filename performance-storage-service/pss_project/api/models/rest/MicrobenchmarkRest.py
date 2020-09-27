from pss_project.api.models.rest.metadata.OLTPBenchMetadata import OLTPBenchMetadata
from pss_project.api.models.rest.parameters.MicrobenchmarkParameters import MicrobenchmarkParameters
from pss_project.api.models.rest.metrics.MicrobenchmarkMetrics import MicrobenchmarkMetrics
from pss_project.api.models.rest.utils import convert_environment_to_dict


class MicrobenchmarkRest(object):
    def __init__(self, metadata, timestamp, parameters, metrics):
        self.metadata = OLTPBenchMetadata(**metadata)
        self.timestamp = timestamp
        self.parameters = MicrobenchmarkParameters(**parameters)
        self.metrics = []
        for benchmark in metrics:
            self.metrics.append(MicrobenchmarkMetrics(**benchmark))

    def convert_to_arr_db_json(self):
        benchmarks_db_json = []
        for benchmark in self.metrics:
            benchmark_suite, benchmark_name = benchmark.name.split('/')
            benchmarks_db_json.append({
                'time': self.timestamp,
                'query_mode': self.parameters.query_mode,
                'jenkins_job_id': self.metadata.jenkins.jenkins_job_id,
                'git_branch': self.metadata.github.git_branch,
                'git_commit_id':  self.metadata.github.git_commit_id,
                'db_version': self.metadata.noisepage.db_version,
                'environment': convert_environment_to_dict(self.metadata.environment),
                'benchmark_suite': benchmark_suite,
                'benchmark_name': benchmark_name,
                'threads': self.parameters.threads,
                'min_runtime': self.parameters.min_runtime,
                'wal_device': self.metadata.environment.wal_device,
                'metrics': benchmark.__dict__,
            })
        return benchmarks_db_json
