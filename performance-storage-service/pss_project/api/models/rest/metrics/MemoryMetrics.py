class MemoryItemSummary:
    """ This class is the model of how summary level memory info is represented in the HTTP API """

    def __init__(self, avg=None):
        if avg:
            self.avg = avg


class MemoryMetrics:
    """ This class is the model of how memory metrics are represented in the HTTP API. Currently, it captures the
    virtual memory size and the resident set size """

    def __init__(self, rss, vms):
        self.rss = rss
        self.vms = vms
