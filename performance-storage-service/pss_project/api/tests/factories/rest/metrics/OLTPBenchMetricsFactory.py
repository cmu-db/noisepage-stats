from factory import Factory, Faker
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics
from pss_project.api.tests.factories.rest.metrics.LatencyMetricsFactory import LatencyMetricsFactory
class OLTPBenchMetricsFactory(Factory):
    class Meta:
        model = OLTPBenchMetrics
    
    throughput = Faker('pydecimal',left_digits=9,right_digits=15, positive=True)
    latency = LatencyMetricsFactory().__dict__