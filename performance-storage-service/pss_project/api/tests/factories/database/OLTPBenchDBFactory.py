from factory import DjangoModelFactory, Faker 
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult
from collections import OrderedDict

class OLTPBenchDBFactory(DjangoModelFactory):
    class Meta:
        model = OLTPBenchResult

    time = Faker('iso8601')
    query_mode = Faker('random_element', elements=('simple', 'extended'))
    jenkins_job_id = Faker('pystr_format',string_format='###')
    git_branch = Faker('word')
    git_commit_id = Faker('sha1')
    db_version = Faker('word')
    environment = Faker('pydict', value_types=[str])
    benchmark_type = Faker('word')
    scale_factor = Faker('pyfloat', left_digits=6,
                         right_digits=4, positive=True)
    terminals = Faker('random_int', min=1, max=16)
    client_time = Faker('random_int', min=30, step=30)
    weights = Faker('pydict',value_types=[int])
    metrics = Faker('pydict', value_types=[int,float])

    # TODO: Do we have a better way to generate an array with random length?
    incremental_metrics = [
        OrderedDict([
            ('bar', '222'),
            ('foo', '333')
        ]),
        OrderedDict([
            ('bar', '333'),
            ('foo', '444')
        ]),
        OrderedDict([
            ('bar', '333'),
            ('foo', '444'),
            ('boo', OrderedDict([
                ('aaa', '111'),
                ('bbb', '222')
            ]))
        ])
    ]