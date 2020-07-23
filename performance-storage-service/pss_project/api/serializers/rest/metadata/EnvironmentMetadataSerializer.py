from rest_framework.serializers import Serializer, CharField
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata


class EnvironmentMetadataSerializer(Serializer):
    # Fields
    os_version = CharField()
    cpu_number = CharField()
    cpu_socket = CharField()

    def create(self, validated_data):
        return EnvironmentMetadata(**validated_data)
