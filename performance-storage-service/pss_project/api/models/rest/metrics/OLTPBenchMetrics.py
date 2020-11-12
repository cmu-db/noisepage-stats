from pss_project.api.models.rest.metrics.SummaryPerformanceMetrics import SummaryPerformanceMetrics
from pss_project.api.models.rest.metrics.IncrementalMetrics import IncrementalMetrics


class OLTPBenchMetrics(SummaryPerformanceMetrics):
    def __init__(self,
                 throughput,
                 latency=None,
                 memory_info=None,
                 incremental_metrics=None):
        super().__init__(throughput, latency, memory_info)
        if incremental_metrics:
            self.incremental_metrics = []
            for metric in incremental_metrics:
                self.incremental_metrics.append(IncrementalMetrics(**metric))
