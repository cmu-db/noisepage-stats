from factory import DjangoModelFactory, Faker
from pss_project.api.models.database.MicrobenchmarkResult import MicrobenchmarkResult


class MicrobenchmarkDBFactory(DjangoModelFactory):
    class Meta:
        model = MicrobenchmarkResult

    time = Faker('iso8601')
    jenkins_job_id = Faker('pystr_format', string_format='###')
    git_branch = Faker('word')
    git_commit_id = Faker('sha1')
    db_version = Faker('word')
    environment = Faker('pydict', value_types=[str])
    benchmark_suite = Faker('word')
    benchmark_name = Faker('word')
    threads = Faker('random_int', min=1, max=16)
    min_runtime = Faker('random_int', min=30, step=30)
    wal_device = Faker('random_element', elements=('RAM disk', 'HDD', 'SATA SSD', 'NVMe SSD', 'None'))
    metrics = Faker('pydict', value_types=[int, float])
