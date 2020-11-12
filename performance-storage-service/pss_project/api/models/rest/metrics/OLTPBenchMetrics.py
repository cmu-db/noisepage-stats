from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics
from pss_project.api.models.rest.metrics.IncrementalMetrics import IncrementalMetrics


class OLTPBenchMetrics(BasePerformanceMetrics):
    def __init__(self, throughput, latency=None, incremental_metrics=None):
        super().__init__(throughput, latency)
        if incremental_metrics:
            self.incremental_metrics = []
            for metric in incremental_metrics:
                self.incremental_metrics.append(
                    IncrementalMetrics(**metric)
                )
