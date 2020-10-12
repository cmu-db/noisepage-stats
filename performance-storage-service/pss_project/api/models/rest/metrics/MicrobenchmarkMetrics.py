from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class MicrobenchmarkMetrics(BasePerformanceMetrics):
    def __init__(self, throughput, status, ref_throughput, stdev_throughput, threshold, iterations):
        super().__init__(throughput)
        self.status = status
        self.ref_throughput = ref_throughput
        self.stdev_throughput = stdev_throughput
        self.threshold = threshold
        self.iterations = iterations
