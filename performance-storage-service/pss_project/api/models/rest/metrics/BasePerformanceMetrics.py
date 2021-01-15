from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics
from pss_project.api.models.rest.metrics.MemoryMetrics import MemoryMetrics


class BasePerformanceMetrics(object):
    """ The base class for performance metrics as communicated through the HTTP API. It includes latency, throughput,
    and memory utilization metrics """

    def __init__(self, throughput, latency=None, memory_info=None):
        self.throughput = throughput
        if latency:
            self.latency = LatencyMetrics(**latency)
        if memory_info:
            self.memory_info = MemoryMetrics(**memory_info)
