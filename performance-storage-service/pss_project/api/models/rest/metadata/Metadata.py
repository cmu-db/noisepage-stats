
from pss_project.api.models.rest.metadata.JenkinsMetadata import JenkinsMetadata
from pss_project.api.models.rest.metadata.GithubMetadata import GithubMetadata
from pss_project.api.models.rest.metadata.NoisePageMetadata import NoisePageMetadata
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata


class Metadata(object):
    """ This class is the model of the all the metadata data as it is represented in the HTTP API
        jenkins - all data relating to the job/build that reported the metrics
        github - all github related info (i.e. branch, commit sha)
        noisepage - all system specific metadata (i.e. DB version)
        environment - all environment metadata relating to the conditions under which the metrics were gathered """

    def __init__(self, jenkins, github, noisepage, environment):
        self.jenkins = JenkinsMetadata(**jenkins)
        self.github = GithubMetadata(**github)
        self.noisepage = NoisePageMetadata(**noisepage)
        self.environment = EnvironmentMetadata(**environment)
