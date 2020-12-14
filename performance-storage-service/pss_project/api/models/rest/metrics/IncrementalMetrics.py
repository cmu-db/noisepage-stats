from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class IncrementalMetrics(BasePerformanceMetrics):
    """ This class is the model of incremental metrics as they are communicated through the HTTP API. The incremental
    metrics are similar to the BasePerformanceMetrics except they have a relative time associated with each entry. The
    time is the number of seconds into the test when the metric instance was gathered. """
    def __init__(self, time, throughput=None, latency=None, memory_info=None):
        self.time = time
        super().__init__(throughput, latency, memory_info)
