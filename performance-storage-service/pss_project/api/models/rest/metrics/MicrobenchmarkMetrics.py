from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class MicrobenchmarkMetrics(BasePerformanceMetrics):
    def __init__(self, throughput, tolerance, iterations, status=None, ref_throughput=None, stdev_throughput=None):
        super().__init__(throughput)
        self.tolerance = tolerance
        self.iterations = iterations
        self.status = status
        self.ref_throughput = ref_throughput
        self.stdev_throughput = stdev_throughput
