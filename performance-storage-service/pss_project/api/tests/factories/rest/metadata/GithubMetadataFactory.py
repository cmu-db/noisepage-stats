from factory import Factory, Faker
from pss_project.api.models.rest.metadata.GithubMetadata import GithubMetadata

class GithubMetadataFactory(Factory):
    class Meta:
        model = GithubMetadata
  
    commit_id = Faker('sha1')
    branch = Faker('word')


        