from pss_project.api.models.rest.BaseRest import BaseRest
from pss_project.api.models.rest.parameters.OLTPBenchParameters import OLTPBenchParameters
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics
from pss_project.api.models.rest.utils import to_dict


class OLTPBenchRest(BaseRest):
    def __init__(self, metadata, timestamp, type, parameters, metrics):
        super().__init__(metadata, timestamp)
        self.type = type
        self.parameters = OLTPBenchParameters(**parameters)
        self.metrics = OLTPBenchMetrics(**metrics)

    def convert_to_db_json(self):
        data = super().convert_to_db_json()
        oltpbench_data = {
            'benchmark_type': self.type,
            'query_mode': self.parameters.query_mode,
            'scale_factor': self.parameters.scale_factor,
            'terminals': self.parameters.terminals,
            'client_time': self.parameters.client_time,
            'weights': convert_weights_to_dict(self.parameters.transaction_weights),
            'wal_device': self.metadata.environment.wal_device,
            'max_connection_threads': self.parameters.max_connection_threads,
            'incremental_metrics': convert_incremental_metrics_to_dict(self.metrics.incremental_metrics)
        }
        data.update(oltpbench_data)
        return data

    def convert_metrics_to_dict(metrics):
        db_formatted_metrics = {
            'throughput': metrics.throughput,
            'latency': metrics.latency.__dict__,
            'memory_info': to_dict(metrics.memory_info),
        }
        return db_formatted_metrics


def convert_weights_to_dict(weights_list):
    db_formatted_weights = {}
    for weight_details in weights_list:
        weight_name = weight_details.name
        weight_value = weight_details.weight
        db_formatted_weights[weight_name] = weight_value
    return db_formatted_weights

def convert_incremental_metrics_to_dict(incremental_metrics):
    db_formatted_incremental_metrics = []
    for metric in incremental_metrics:
        db_formatted_incremental_json = {
            'time': metric.time,
            'throughput': metric.throughput,
            'latency': metric.latency.__dict__,
            'memory_info': metric.memory_info.__dict__,
        }
        db_formatted_incremental_metrics.append(db_formatted_incremental_json)
    return db_formatted_incremental_metrics
