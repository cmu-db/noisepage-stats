class MicrobenchmarkParameters(object):
    def __init__(self, query_mode, threads, min_runtime):
        self.query_mode = query_mode
        self.threads = threads
        self.min_runtime = min_runtime
