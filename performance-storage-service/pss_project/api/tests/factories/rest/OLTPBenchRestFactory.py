from factory import Factory, SubFactory, Faker
from pss_project.api.models.rest.OLTPBenchRest import OLTPBenchRest
from pss_project.api.tests.factories.rest.metadata.OLTPBenchMetadataFactory \
     import OLTPBenchMetadataFactory
from pss_project.api.tests.factories.rest.parameters.OLTPBenchParameters \
    import OLTPBenchParametersFactory
from pss_project.api.tests.factories.rest.metrics.OLTPBenchMetricsFactory \
    import OLTPBenchMetricsFactory


class OLTPBenchRestFactory(Factory):
    class Meta:
        model = OLTPBenchRest

    metadata = SubFactory(OLTPBenchMetadataFactory)
    timestamp = Faker('date_time')
    type = Faker('word')
    parameters = SubFactory(OLTPBenchParametersFactory)
    metrics = SubFactory(OLTPBenchMetricsFactory)
