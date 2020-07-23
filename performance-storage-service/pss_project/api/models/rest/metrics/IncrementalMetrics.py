from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics


class IncrementalMetrics(object):
    def __init__(self, time, throughput, latency=None):
        self.time = time
        self.throughput = throughput
        if latency:
            self.latency = LatencyMetrics(**latency).__dict__
