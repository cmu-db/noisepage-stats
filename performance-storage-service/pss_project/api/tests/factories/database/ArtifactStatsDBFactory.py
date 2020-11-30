from django.utils import timezone
from factory import Faker
from factory.django import DjangoModelFactory
from pss_project.api.models.database.ArtifactStatsResult import ArtifactStatsResult


class ArtifactStatsDBFactory(DjangoModelFactory):
    class Meta:
        model = ArtifactStatsResult

    time = Faker('iso8601', tzinfo=timezone.utc)
    jenkins_job_id = Faker('pystr_format', string_format='###')
    git_branch = Faker('word')
    git_commit_id = Faker('sha1')
    db_version = Faker('word')
    environment = Faker('pydict', value_types=[str])
    metrics = Faker('pydict', value_types=[int, float, str, [], dict])
