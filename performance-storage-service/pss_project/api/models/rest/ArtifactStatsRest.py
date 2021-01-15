from pss_project.api.models.rest.BaseRest import BaseRest


class ArtifactStatsRest(BaseRest):
    """ This class is the model of the Artifact Stats data as it is communicated through the HTTP API """

    def __init__(self, metadata, timestamp, metrics):
        super().__init__(metadata, timestamp)
        self.metrics = metrics

    def convert_metrics_to_dict(self, metrics):
        """ Override the base class method """
        return metrics
