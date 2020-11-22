class MemoryItemSummary:
    def __init__(self, avg=None):
        if avg:
            self.avg = avg


class MemoryMetrics:
    def __init__(self, rss, vms):
        self.rss = rss
        self.vms = vms
