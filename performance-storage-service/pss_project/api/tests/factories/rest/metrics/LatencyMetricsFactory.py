from factory import Factory, Faker
from pss_project.api.models.rest.metrics.LatencyMetrics import LatencyMetrics


class LatencyMetricsFactory(Factory):
    class Meta:
        model = LatencyMetrics

    l_25 = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    l_75 = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    l_90 = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    l_95 = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    l_99 = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    avg = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    median = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    max = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
    min = Faker('pydecimal', left_digits=6, right_digits=4, positive=True)
