from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class MicrobenchmarkMetrics(BasePerformanceMetrics):
    def __init__(self, name, throughput, iterations=None, real_time=None, cpu_time=None, bytes_per_second=None):
        super().__init__(throughput)
        self.name = name
        self.throughput = throughput
        if iterations:
            self.iterations = iterations
        if real_time:
            self.real_time = real_time
        if cpu_time:
            self.cpu_time = cpu_time
        if bytes_per_second:
            self.bytes_per_second = bytes_per_second
