from factory import Factory, SubFactory
from pss_project.api.models.rest.metadata.OLTPBenchMetadata import OLTPBenchMetadata
from pss_project.api.tests.factories.rest.metadata.JenkinsMetadataFactory import JenkinsMetadataFactory
from pss_project.api.tests.factories.rest.metadata.GithubMetadataFactory import GithubMetadataFactory
from pss_project.api.tests.factories.rest.metadata.NoisePageMetadataFactory import NoisePageMetadataFactory

class OLTPBenchMetadataFactory(Factory):
    class Meta:
        model = OLTPBenchMetadata

    jenkins = SubFactory(JenkinsMetadataFactory)
    github = SubFactory(GithubMetadataFactory)
    noisepage = SubFactory(NoisePageMetadataFactory)