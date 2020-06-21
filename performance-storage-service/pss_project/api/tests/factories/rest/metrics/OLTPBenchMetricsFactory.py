from factory import Factory, Faker
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics

class OLTPBenchMetricsFactory(Factory):
    class Meta:
        model = OLTPBenchMetrics
    
    throughput = Faker('pydecimal',left_digits=9,right_digits=15, positive=True)
    latency_99 = Faker('random_int')
    latency_95 = Faker('random_int')
    latency_avg = Faker('random_int')
    latency_max = Faker('random_int')