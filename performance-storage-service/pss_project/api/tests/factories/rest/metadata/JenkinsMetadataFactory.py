from factory import Factory, Faker
from pss_project.api.models.rest.metadata.JenkinsMetadata import JenkinsMetadata


class JenkinsMetadataFactory(Factory):
    class Meta:
        model = JenkinsMetadata
    
    jenkins_job_id = Faker('pystr_format',string_format='###')
