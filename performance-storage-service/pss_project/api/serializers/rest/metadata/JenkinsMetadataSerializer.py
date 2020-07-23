from rest_framework.serializers import Serializer, CharField
from pss_project.api.models.rest.metadata.JenkinsMetadata import JenkinsMetadata


class JenkinsMetadataSerializer(Serializer):
    # Fields
    jenkins_job_id = CharField()

    def create(self, validated_data):
        return JenkinsMetadata(**validated_data)
