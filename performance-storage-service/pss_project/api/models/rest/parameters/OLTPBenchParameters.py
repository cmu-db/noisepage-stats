from pss_project.api.models.rest.parameters.TransactionWeight import TransactionWeight


class OLTPBenchParameters(object):
    def __init__(self, query_mode, scale_factor, terminals, duration, transaction_weights):
        self.query_mode = query_mode
        self.scale_factor = scale_factor
        self.terminals = terminals
        self.duration = duration
        self.transaction_weights = []
        for weight in transaction_weights:
            self.transaction_weights.append(
                TransactionWeight(**weight)
            )
