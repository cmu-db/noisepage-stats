from pss_project.api.models.rest.metadata.OLTPBenchMetadata import OLTPBenchMetadata
from pss_project.api.models.rest.parameters.OLTPBenchParameters import OLTPBenchParameters
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics
from pss_project.api.models.rest.utils import convert_environment_to_dict


class OLTPBenchRest(object):
    def __init__(self, metadata, timestamp, type, parameters, metrics):
        self.metadata = OLTPBenchMetadata(**metadata)
        self.timestamp = timestamp
        self.type = type
        self.parameters = OLTPBenchParameters(**parameters)
        self.metrics = OLTPBenchMetrics(**metrics)

    def convert_to_db_json(self):
        data = {
            'time': self.timestamp,
            'git_branch': self.metadata.github.git_branch,
            'git_commit_id': self.metadata.github.git_commit_id,
            'jenkins_job_id': self.metadata.jenkins.jenkins_job_id,
            'db_version': self.metadata.noisepage.db_version,
            'environment': convert_environment_to_dict(self.metadata.environment),
            'benchmark_type': self.type,
            'query_mode': self.parameters.query_mode,
            'scale_factor': self.parameters.scale_factor,
            'terminals': self.parameters.terminals,
            'client_time': self.parameters.client_time,
            'weights': convert_weights_to_dict(self.parameters.transaction_weights),
            'wal_device': self.metadata.environment.wal_device,
            'max_connection_threads': self.parameters.max_connection_threads,
            'metrics': convert_metrics_to_dict(self.metrics),
            'incremental_metrics': convert_incremental_metrics_to_dict(self.metrics.incremental_metrics)
        }
        return data


def convert_weights_to_dict(weights_list):
    db_formatted_weights = {}
    for weight_details in weights_list:
        weight_name = weight_details.name
        weight_value = weight_details.weight
        db_formatted_weights[weight_name] = weight_value
    return db_formatted_weights


def convert_metrics_to_dict(metrics):
    db_formatted_metrics = {
        'throughput': metrics.throughput,
        'latency': metrics.latency.__dict__
    }
    return db_formatted_metrics


def convert_incremental_metrics_to_dict(incremental_metrics):
    db_formatted_incremental_metrics = []
    for metric in incremental_metrics:
        db_formatted_incremental_json = {
            'time': metric.time,
            'throughput': metric.throughput,
            'latency': metric.latency.__dict__
        }
        db_formatted_incremental_metrics.append(db_formatted_incremental_json)
    return db_formatted_incremental_metrics
