from factory import Factory, Faker
from pss_project.api.models.rest.ArtifactStatsRest import ArtifactStatsRest
from pss_project.api.tests.factories.rest.metadata.MetadataFactory \
    import MetadataFactory
from pss_project.api.tests.utils.utils import generate_dict_factory


class ArtifactStatsRestFactory(Factory):
    class Meta:
        model = ArtifactStatsRest
    metadata = generate_dict_factory(MetadataFactory)()
    timestamp = Faker('date_time')
    metrics = Faker('pydict', value_types=[int, float, str, [], dict])
