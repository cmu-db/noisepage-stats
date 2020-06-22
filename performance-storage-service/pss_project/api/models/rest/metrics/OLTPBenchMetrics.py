class OLTPBenchMetrics(object):
    def __init__(self, throughput, latency_99=None, latency_95=None, latency_avg=None, latency_max=None):
        self.throughput = throughput
        if latency_99:
            self.latency_99 = latency_99
        if latency_95:
            self.latency_95 = latency_95
        if latency_avg:
            self.latency_avg = latency_avg
        if latency_max:
            self.latency_max = latency_max