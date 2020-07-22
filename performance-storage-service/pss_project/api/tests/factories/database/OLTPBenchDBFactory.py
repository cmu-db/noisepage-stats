from factory import DjangoModelFactory, Faker
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult


class OLTPBenchDBFactory(DjangoModelFactory):
    class Meta:
        model = OLTPBenchResult

    time = Faker('iso8601')
    branch = Faker('word')
    query_mode = Faker('random_element', elements=('simple', 'extended'))
    build_id = Faker('pystr_format', string_format='###')
    git_commit_id = Faker('sha1')
    benchmark_type = Faker('word')
    scale_factor = Faker('pyfloat', left_digits=6,
                         right_digits=4, positive=True)
    terminals = Faker('random_int', min=1, max=16)
    duration = Faker('random_int', min=30, step=30)
    weights = Faker('pydict', value_types=[int])
    metrics = Faker('pydict', value_types=[int, float])
