class MicrobenchmarkParameters(object):
    """ This class is the model of the microbenchmark parameters as communicated through the HTTP API """

    def __init__(self, threads, min_runtime):
        self.threads = threads
        self.min_runtime = min_runtime
