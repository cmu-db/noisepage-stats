from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics
from pss_project.api.models.rest.metrics.MemoryMetrics import MemoryMetrics


class BasePerformanceMetrics(object):
    def __init__(self, throughput, latency=None, memory_info=None):
        self.throughput = throughput
        if latency:
            self.latency = LatencyMetrics(**latency)
        if memory_info:
            self.memory_info = MemoryMetrics(**memory_info)
