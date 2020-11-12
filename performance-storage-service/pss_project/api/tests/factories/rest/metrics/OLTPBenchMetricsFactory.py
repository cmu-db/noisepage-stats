from factory import Factory, Faker
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics
from pss_project.api.tests.factories.rest.metrics.LatencyMetricsFactory import LatencyMetricsFactory
from pss_project.api.tests.factories.rest.metrics.MemoryMetricsFactory import MemorySummaryMetricsFactory
from pss_project.api.tests.factories.rest.metrics.IncrementalMetricsFactory import IncrementalMetricsFactory
from pss_project.api.tests.utils.utils import generate_dict_factory


class OLTPBenchMetricsFactory(Factory):
    class Meta:
        model = OLTPBenchMetrics

    throughput = Faker('pydecimal',
                       left_digits=9,
                       right_digits=15,
                       positive=True)
    latency = LatencyMetricsFactory().__dict__
    memory_info = MemorySummaryMetricsFactory().__dict__
    incremental_metrics = Faker(
        'random_elements',
        elements=(
            generate_dict_factory(IncrementalMetricsFactory)(),
            generate_dict_factory(IncrementalMetricsFactory)(),
            generate_dict_factory(IncrementalMetricsFactory)(),
            generate_dict_factory(IncrementalMetricsFactory)(),
            generate_dict_factory(IncrementalMetricsFactory)(),
        ),
        unique=True)
