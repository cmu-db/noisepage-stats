from factory import Factory, Faker
from pss_project.api.models.rest.MicrobenchmarkRest import MicrobenchmarkRest
from pss_project.api.tests.factories.rest.metadata.MetadataFactory \
    import MetadataFactory
from pss_project.api.tests.factories.rest.parameters.MicrobenchmarkParametersFactory \
    import MicrobenchmarkParametersFactory
from pss_project.api.tests.factories.rest.metrics.MicrobenchmarkMetricsFactory \
    import MicrobenchmarkMetricsFactory
from pss_project.api.tests.utils.utils import generate_dict_factory


class MicrobenchmarkRestFactory(Factory):
    class Meta:
        model = MicrobenchmarkRest
    metadata = generate_dict_factory(MetadataFactory)()
    timestamp = Faker('date_time')
    parameters = generate_dict_factory(MicrobenchmarkParametersFactory)()
    metrics = Faker('random_elements', elements=(
        generate_dict_factory(MicrobenchmarkMetricsFactory)(),
        generate_dict_factory(MicrobenchmarkMetricsFactory)(),
        generate_dict_factory(MicrobenchmarkMetricsFactory)(),
        generate_dict_factory(MicrobenchmarkMetricsFactory)(),
        generate_dict_factory(MicrobenchmarkMetricsFactory)(),
    ), unique=True)
