from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class IncrementalMetrics(BasePerformanceMetrics):
    def __init__(self, time, throughput=None, latency=None):
        self.time = time
        super().__init__(throughput, latency)
