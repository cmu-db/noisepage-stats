from pss_project.api.models.rest.BaseRest import BaseRest


class BinaryMetricsRest(BaseRest):
    def __init__(self, metadata, timestamp, metrics):
        super().__init__(metadata, timestamp)
        self.metrics = metrics

    def convert_metrics_to_dict(self, metrics):
        return metrics
