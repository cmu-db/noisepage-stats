from factory import Factory, Faker
from pss_project.api.models.rest.metrics.IncrementalMetrics import IncrementalMetrics
from pss_project.api.tests.factories.rest.metrics.LatencyMetricsFactory \
    import LatencyMetricsFactory
from pss_project.api.tests.factories.rest.metrics.MemoryMetricsFactory \
    import MemoryMetricsFactory


class IncrementalMetricsFactory(Factory):
    class Meta:
        model = IncrementalMetrics

    time = Faker('random_int')
    throughput = Faker('pydecimal',
                       left_digits=9,
                       right_digits=15,
                       positive=True)
    latency = LatencyMetricsFactory().__dict__
    memory_info = MemoryMetricsFactory().__dict__
