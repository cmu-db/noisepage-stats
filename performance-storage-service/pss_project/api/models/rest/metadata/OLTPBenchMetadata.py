
from pss_project.api.models.rest.metadata.JenkinsMetadata import JenkinsMetadata
from pss_project.api.models.rest.metadata.GithubMetadata import GithubMetadata
from pss_project.api.models.rest.metadata.NoisePageMetadata import NoisePageMetadata


class OLTPBenchMetadata(object):
    def __init__(self, jenkins, github, noisepage):
        self.jenkins = JenkinsMetadata(**jenkins)
        self.github = GithubMetadata(**github)
        self.noisepage = NoisePageMetadata(**noisepage)
