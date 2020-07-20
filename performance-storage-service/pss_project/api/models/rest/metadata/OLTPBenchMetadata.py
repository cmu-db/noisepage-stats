
from pss_project.api.models.rest.metadata.JenkinsMetadata import JenkinsMetadata
from pss_project.api.models.rest.metadata.GithubMetadata import GithubMetadata
from pss_project.api.models.rest.metadata.NoisePageMetadata import NoisePageMetadata
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata

class OLTPBenchMetadata(object):
    def __init__(self, jenkins, github, noisepage, environment):
        self.jenkins = JenkinsMetadata(**jenkins)
        self.github = GithubMetadata(**github) 
        self.noisepage = NoisePageMetadata(**noisepage)
        self.environment = EnvironmentMetadata(**environment)
    