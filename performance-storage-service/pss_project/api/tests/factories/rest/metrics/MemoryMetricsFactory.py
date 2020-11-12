from factory import Factory, Faker
from pss_project.api.models.rest.metrics.MemoryMetrics import MemoryMetrics, MemoryItemSummary


class MemoryInfoSummaryFactory(Factory):
    class Meta:
        model = MemoryItemSummary

    avg = Faker('pydecimal', left_digits=10, right_digits=4, positive=True)


class MemoryMetricsFactory(Factory):
    class Meta:
        model = MemoryMetrics

    rss = Faker('random_int')
    vms = Faker('random_int')


class MemorySummaryMetricsFactory(Factory):
    class Meta:
        model = MemoryMetrics

    rss = MemoryInfoSummaryFactory().__dict__
    vms = MemoryInfoSummaryFactory().__dict__