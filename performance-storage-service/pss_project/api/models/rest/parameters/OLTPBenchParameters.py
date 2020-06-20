class OLTPBenchParameters(object):
    def __init__(self, query_mode, scale_factor, terminals, duration, transaction_weights):
        self.query_mode = query_mode
        self.scale_factor = scale_factor
        self.terminals = terminals
        self.duration = duration
        self.transaction_weights = transaction_weights