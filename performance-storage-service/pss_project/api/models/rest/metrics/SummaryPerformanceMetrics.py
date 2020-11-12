from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics
from pss_project.api.models.rest.metrics.MemoryMetrics import MemoryMetrics, MemoryItemSummary


class SummaryPerformanceMetrics(BasePerformanceMetrics):
    def __init__(self, throughput, latency=None, memory_info=None):
        super().__init__(throughput, latency)
        if memory_info:
            rss = MemoryItemSummary(
                **memory_info["rss"]) if "rss" in memory_info else None
            vms = MemoryItemSummary(
                **memory_info["vms"]) if "vms" in memory_info else None
            self.memory_info = MemoryMetrics(rss, vms)
