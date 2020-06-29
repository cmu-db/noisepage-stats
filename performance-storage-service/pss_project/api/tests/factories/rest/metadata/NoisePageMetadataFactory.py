from factory import Factory, Faker
from pss_project.api.models.rest.metadata.NoisePageMetadata import NoisePageMetadata

class NoisePageMetadataFactory(Factory):
    class Meta:
        model = NoisePageMetadata

    version = Faker('pystr_format',string_format='##.#')