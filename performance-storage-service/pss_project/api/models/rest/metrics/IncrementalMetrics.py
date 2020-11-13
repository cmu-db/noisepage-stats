from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class IncrementalMetrics(BasePerformanceMetrics):
    def __init__(self, time, throughput=None, latency=None, memory_info=None):
        self.time = time
        super().__init__(throughput, latency, memory_info)
