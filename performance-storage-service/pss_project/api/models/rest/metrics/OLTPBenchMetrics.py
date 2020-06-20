class OLTPBenchMetrics(object):
    def __init__(self, throughput, latency_99, latency_95, latency_avg, latency_max):
        self.throughput = throughput
        self.latency_99 = latency_99
        self.latency_95 = latency_95
        self.latency_avg = latency_avg
        self.latency_max = latency_max