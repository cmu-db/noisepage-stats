class OLTPBenchRest(object):
    def __init__(self, metadata, timestamp, type, parameters, metrics):
        self.metadata = metadata
        self.timestamp = timestamp
        self.type = type
        self.parameters = parameters
        self.metrics = metrics 