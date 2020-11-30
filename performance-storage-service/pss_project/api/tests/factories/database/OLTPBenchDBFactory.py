from factory import Faker, Dict
from factory.django import DjangoModelFactory
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult

class OLTPBenchDBFactory(DjangoModelFactory):
    class Meta:
        model = OLTPBenchResult
        django_get_or_create = ('git_branch','git_commit_id',)

    time = Faker('iso8601')
    query_mode = Faker('random_element', elements=('simple', 'extended'))
    jenkins_job_id = Faker('pystr_format', string_format='###')
    git_branch = Faker('word')
    git_commit_id = Faker('sha1')
    db_version = Faker('word')
    environment = Faker('pydict', value_types=[str])
    benchmark_type = Faker('word')
    scale_factor = Faker('pyfloat', left_digits=6,
                         right_digits=4, positive=True)
    terminals = Faker('random_int', min=1, max=32)
    client_time = Faker('random_int', min=30, step=30)
    weights = Faker('pydict', value_types=[int])
    wal_device = Faker('random_element', elements=('RAM disk', 'HDD', 'SATA SSD', 'NVMe SSD', 'None'))
    max_connection_threads = Faker('random_int', min=1, max=32)
    metrics = Dict({
        'throughput':Faker('pyfloat',positive=True),
        'latency':Faker('pydict',value_types=[float])
    })
    incremental_metrics = Faker('pydict', value_types=[int, float, str])
