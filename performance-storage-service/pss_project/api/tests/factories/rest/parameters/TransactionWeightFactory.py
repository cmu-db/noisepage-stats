from factory import Factory, Faker
from pss_project.api.models.rest.parameters.TransactionWeight import TransactionWeight


class TransactionWeightFactory(Factory):
    class Meta:
        model = TransactionWeight

    name = Faker('word')
    weight = Faker('random_int', min=1, max=100)