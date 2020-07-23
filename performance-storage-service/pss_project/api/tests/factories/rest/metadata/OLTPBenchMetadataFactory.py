from factory import Factory, SubFactory
from pss_project.api.models.rest.metadata.OLTPBenchMetadata import OLTPBenchMetadata
from pss_project.api.tests.factories.rest.metadata.JenkinsMetadataFactory import JenkinsMetadataFactory
from pss_project.api.tests.factories.rest.metadata.GithubMetadataFactory import GithubMetadataFactory
from pss_project.api.tests.factories.rest.metadata.NoisePageMetadataFactory import NoisePageMetadataFactory
from pss_project.api.tests.factories.rest.metadata.EnvironmentMetadataFactory import EnvironmentMetadataFactory

class OLTPBenchMetadataFactory(Factory):
    class Meta:
        model = OLTPBenchMetadata

    jenkins = JenkinsMetadataFactory().__dict__
    github = GithubMetadataFactory().__dict__
    noisepage = NoisePageMetadataFactory().__dict__
    environment = EnvironmentMetadataFactory().__dict__
