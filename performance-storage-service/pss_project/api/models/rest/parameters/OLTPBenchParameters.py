from pss_project.api.models.rest.parameters.TransactionWeight import TransactionWeight


class OLTPBenchParameters(object):
    def __init__(self, query_mode, scale_factor, terminals, client_time, transaction_weights,
                 wal_device, max_connection_threads):
        self.query_mode = query_mode
        self.scale_factor = scale_factor
        self.terminals = terminals
        self.client_time = client_time
        self.transaction_weights = []
        for weight in transaction_weights:
            self.transaction_weights.append(
                TransactionWeight(**weight)
            )
        self.wal_device = wal_device
        self.max_connection_threads = max_connection_threads
