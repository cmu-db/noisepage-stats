from factory import Factory, Faker
from pss_project.api.models.rest.metrics.MicrobenchmarkMetrics import MicrobenchmarkMetrics


class MicrobenchmarkMetricsFactory(Factory):
    class Meta:
        model = MicrobenchmarkMetrics

    name = '{}/{}'.format(Faker('city').generate(), Faker('word').generate())
    throughput = Faker('pydecimal', left_digits=9, right_digits=15, positive=True)
    iterations = Faker('random_int')
    real_time = Faker('random_int')
    cpu_time = Faker('random_int')
    bytes_per_second = Faker('pydecimal', left_digits=9, right_digits=9, positive=True)
