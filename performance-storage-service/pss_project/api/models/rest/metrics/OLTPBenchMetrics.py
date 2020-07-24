from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics
from pss_project.api.models.rest.metrics.IncrementalMetrics import IncrementalMetrics


class OLTPBenchMetrics(object):
    def __init__(self, throughput, incremental_metrics=None, latency=None):
        self.throughput = throughput
        if latency:
            self.latency = LatencyMetrics(**latency)
        if incremental_metrics:
            self.incremental_metrics = []
            for metric in incremental_metrics:
                self.incremental_metrics.append(
                    IncrementalMetrics(**metric)
                )
