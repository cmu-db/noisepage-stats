from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics

class OLTPBenchMetrics(object):
    def __init__(self, throughput, latency=None):
        self.throughput = throughput
        if latency:
            self.latency = LatencyMetrics(**latency)