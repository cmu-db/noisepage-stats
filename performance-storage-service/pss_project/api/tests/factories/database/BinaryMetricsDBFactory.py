from factory import DjangoModelFactory, Faker
from pss_project.api.models.database.BinaryMetricsResult import BinaryMetricsResult


class BinaryMetricsDBFactory(DjangoModelFactory):
    class Meta:
        model = BinaryMetricsResult

    time = Faker('iso8601')
    jenkins_job_id = Faker('pystr_format', string_format='###')
    git_branch = Faker('word')
    git_commit_id = Faker('sha1')
    db_version = Faker('word')
    environment = Faker('pydict', value_types=[str])
    metrics = Faker('pydict', value_types=[int, float, str, [], dict])
