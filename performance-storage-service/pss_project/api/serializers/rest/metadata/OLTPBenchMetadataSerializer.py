from rest_framework.serializers import Serializer
from pss_project.api.serializers.rest.metadata.JenkinsMetadataSerializer import JenkinsMetadataSerializer
from pss_project.api.serializers.rest.metadata.GithubMetadataSerializer import GithubMetadataSerializer
from pss_project.api.serializers.rest.metadata.NoisePageMetadataSerializer import NoisePageMetadataSerializer
from pss_project.api.serializers.rest.metadata.EnvironmentMetadataSerializer import EnvironmentMetadataSerializer
from pss_project.api.models.rest.metadata.OLTPBenchMetadata import OLTPBenchMetadata


class OLTPBenchMetadataSerializer(Serializer):
    # Fields
    jenkins = JenkinsMetadataSerializer()
    github = GithubMetadataSerializer()
    noisepage = NoisePageMetadataSerializer()
    environment = EnvironmentMetadataSerializer()

    def create(self, validated_data):
        return OLTPBenchMetadata(**validated_data)
