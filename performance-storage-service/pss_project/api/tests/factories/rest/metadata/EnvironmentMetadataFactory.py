from factory import Factory, Faker
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata

class EnvironmentMetadataFactory(Factory):
    class Meta:
        model = EnvironmentMetadata
  
    os_version = Faker('word')
    cpu_number = Faker('random_int', min=1, max=16)
    numa_info = Faker('word')
