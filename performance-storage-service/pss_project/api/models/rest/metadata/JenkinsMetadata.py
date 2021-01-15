class JenkinsMetadata(object):
    """ This class is the model of the Jenkins data relating to the build that ran the tests or collected the metrics.
    This class is how the model is represented in the HTTP API """

    def __init__(self, jenkins_job_id):
        self.jenkins_job_id = jenkins_job_id
