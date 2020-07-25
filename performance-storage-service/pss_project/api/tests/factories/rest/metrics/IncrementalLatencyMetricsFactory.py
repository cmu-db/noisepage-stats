from factory import Factory, Faker
from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics


class IncrementalLatencyMetricsFactory(Factory):
    class Meta:
        model = LatencyMetrics

    l_25 = Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    l_75 = Faker('pydecimal', left_digits=2, right_digits=3, positive=True)
    l_90 = Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    l_95 = Faker('pydecimal', left_digits=3, right_digits=3, positive=True)
    l_99 = Faker('pydecimal', left_digits=5, right_digits=3, positive=True)
    avg = Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    median = Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    max = Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
    min = Faker('pydecimal', left_digits=1, right_digits=3, positive=True)
