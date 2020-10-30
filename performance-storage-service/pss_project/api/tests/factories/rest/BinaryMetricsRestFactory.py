from factory import Factory, Faker
from pss_project.api.models.rest.BinaryMetricsRest import BinaryMetricsRest
from pss_project.api.tests.factories.rest.metadata.MetadataFactory \
    import MetadataFactory
from pss_project.api.tests.utils.utils import generate_dict_factory


class BinaryMetricsRestFactory(Factory):
    class Meta:
        model = BinaryMetricsRest
    metadata = generate_dict_factory(MetadataFactory)()
    timestamp = Faker('date_time')
    metrics = Faker('pydict', value_types=[int, float, str, [], dict])
