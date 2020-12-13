from pss_project.api.models.rest.BaseRest import BaseRest
from pss_project.api.models.rest.parameters.MicrobenchmarkParameters import MicrobenchmarkParameters
from pss_project.api.models.rest.metrics.MicrobenchmarkMetrics import MicrobenchmarkMetrics


class MicrobenchmarkRest(BaseRest):
    """ This class is the model of the Microbench data as it is communicated through the HTTP API """
    def __init__(self, metadata, timestamp, test_suite, test_name, parameters, metrics):
        super().__init__(metadata, timestamp)
        self.test_suite = test_suite
        self.test_name = test_name
        self.parameters = MicrobenchmarkParameters(**parameters)
        self.metrics = MicrobenchmarkMetrics(**metrics)

    def convert_to_db_json(self):
        """ Convert the API model into a dict that can be used to instantiate a MicrobenchmarkResult object """
        data = super().convert_to_db_json()
        microbench_data = {
            'benchmark_suite': self.test_suite,
            'benchmark_name': self.test_name,
            'threads': self.parameters.threads,
            'min_runtime': self.parameters.min_runtime,
            'wal_device': self.metadata.environment.wal_device,
        }
        data.update(microbench_data)
        return data
