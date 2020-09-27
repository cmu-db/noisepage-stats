from factory import Factory, Faker
from pss_project.api.models.rest.OLTPBenchRest import OLTPBenchRest
from pss_project.api.tests.factories.rest.metadata.MetadataFactory \
    import MetadataFactory
from pss_project.api.tests.factories.rest.parameters.OLTPBenchParametersFactory \
    import OLTPBenchParametersFactory
from pss_project.api.tests.factories.rest.metrics.OLTPBenchMetricsFactory \
    import OLTPBenchMetricsFactory
from pss_project.api.tests.utils.utils import generate_dict_factory


class OLTPBenchRestFactory(Factory):
    class Meta:
        model = OLTPBenchRest

    metadata = generate_dict_factory(MetadataFactory)()
    timestamp = Faker('date_time')
    type = Faker('word')
    parameters = generate_dict_factory(OLTPBenchParametersFactory)()
    metrics = generate_dict_factory(OLTPBenchMetricsFactory)()
