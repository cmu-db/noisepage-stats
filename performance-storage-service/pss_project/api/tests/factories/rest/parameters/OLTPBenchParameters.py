from factory import Factory, Faker
from pss_project.api.models.rest.parameters.OLTPBenchParameters import (
    OLTPBenchParameters)
from pss_project.api.tests.factories.rest.parameters.TransactionWeightFactory \
    import (TransactionWeightFactory)


class OLTPBenchParametersFactory(Factory):
    class Meta:
        model = OLTPBenchParameters

    query_mode = Faker('random_element', elements=('simple', 'extended'))
    scale_factor = Faker('pydecimal', left_digits=6,
                         right_digits=4, positive=True)
    terminals = Faker('random_int', min=1, max=16)
    client_time = Faker('random_int', min=30, step=30)
    transaction_weights = Faker('random_elements', elements=(
        TransactionWeightFactory().__dict__,
        TransactionWeightFactory().__dict__,
        TransactionWeightFactory().__dict__,
        TransactionWeightFactory().__dict__,
        TransactionWeightFactory().__dict__,
    ), unique=True)
    wal_device = Faker('random_element', elements=('RAM disk', 'HDD', 'SATA SSD', 'NVMe SSD'))
    max_connection_threads = Faker('random_int', min=1, max=32)
