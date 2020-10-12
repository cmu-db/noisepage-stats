from factory import Factory, Faker
from pss_project.api.models.rest.parameters.MicrobenchmarkParameters import (
    MicrobenchmarkParameters)


class MicrobenchmarkParametersFactory(Factory):
    class Meta:
        model = MicrobenchmarkParameters

    threads = Faker('random_int', min=1, max=16)
    min_runtime = Faker('random_int', min=30, step=30)
