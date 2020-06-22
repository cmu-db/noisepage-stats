from pss_project.api.models.rest.metadata.OLTPBenchMetadata import OLTPBenchMetadata
from pss_project.api.models.rest.parameters.OLTPBenchParameters import OLTPBenchParameters
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics

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
            'branch': self.metadata.github.branch,
            'query_mode': self.parameters.query_mode,
            'build_id': self.metadata.jenkins.build_id,
            'git_commit_id': self.metadata.github.commit_id,
            'benchmark_type': self.type,
            'scale_factor': self.parameters.scale_factor,
            'terminals': self.parameters.terminals,
            'duration': self.parameters.duration,
            'weights': convert_weights_to_dict(self.parameters.transaction_weights),
            'metrics': self.metrics.__dict__,
        }
        return data

def convert_weights_to_dict( weights_list ):
    db_formatted_weights = {}
    for weight_details in weights_list:
        weight_name = weight_details.name
        weight_value = weight_details.weight
        db_formatted_weights[weight_name] = weight_value
    return db_formatted_weights