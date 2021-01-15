from pss_project.api.models.rest.metrics.BasePerformanceMetrics import BasePerformanceMetrics


class MicrobenchmarkMetrics(BasePerformanceMetrics):
    """ This class is the model of the microbenchmark metrics as represented in the HTTP API
            tolerance - the manually set % decrease in performance that is allowed
            iterations - the number of time the microbenchmark was run to get a statistically meaningful result.
            status - PASS or FAIL which is determined by whether the manual tolerance is violated
            ref_throughput - the 30 day rolling average of the microbenchmark
            stdev_throughput - the standard deviation of the last 30 days of results
    """

    def __init__(self, throughput, tolerance, iterations, status=None, ref_throughput=None, stdev_throughput=None):
        super().__init__(throughput)
        self.tolerance = tolerance
        self.iterations = iterations
        self.status = status
        self.ref_throughput = ref_throughput
        self.stdev_throughput = stdev_throughput
