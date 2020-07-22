from factory import Factory, Faker
from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics


class LatencyMetricsFactory(Factory):
    class Meta:
        model = LatencyMetrics

    l_25 = Faker('random_int')
    l_75 = Faker('random_int')
    l_90 = Faker('random_int')
    l_95 = Faker('random_int')
    l_99 = Faker('random_int')
    avg = Faker('random_int')
    median = Faker('random_int')
    max = Faker('random_int')
    min = Faker('random_int')
