from pss_project.api.models.rest.metadata.Metadata import Metadata


class BaseRest(object):
    """ The based class for all objects communicated through the HTTP API """

    def __init__(self, metadata, timestamp):
        self.metadata = Metadata(**metadata)
        self.timestamp = timestamp

    def convert_to_db_json(self):
        """ Convert the base class attributes into a dict that can be used to instantiate database object models """
        data = {
            'time': self.timestamp,
            'git_branch': self.metadata.github.git_branch,
            'git_commit_id': self.metadata.github.git_commit_id,
            'jenkins_job_id': self.metadata.jenkins.jenkins_job_id,
            'db_version': self.metadata.noisepage.db_version,
            'environment': convert_environment_to_dict(self.metadata.environment),
            'metrics': self.convert_metrics_to_dict(self.metrics),
        }
        return data

    def convert_metrics_to_dict(self, metrics):
        """ Convert the metrics object to a dict. This should be overridden when the metrics JSON is nested or has a
        special format """
        return metrics.__dict__


def convert_environment_to_dict(environment):
    db_formatted_environment = {
        'os_version': environment.os_version,
        'cpu_number': environment.cpu_number,
        'cpu_socket': environment.cpu_socket
    }
    return db_formatted_environment
