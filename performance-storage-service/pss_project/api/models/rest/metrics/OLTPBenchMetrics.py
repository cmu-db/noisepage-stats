from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics

class OLTPBenchMetrics(object):
    def __init__(self, throughput, incremental_metrics, latency=None):
        self.throughput = throughput
        if latency:
            self.latency = LatencyMetrics(**latency)
        self.incremental_metrics = [dict(metric) for metric in incremental_metrics]