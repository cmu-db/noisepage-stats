from rest_framework.serializers import Serializer, CharField 
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata

class EnvironmentMetadataSerializer(Serializer):
    # Fields
    os_version = CharField()
    cpu_number = CharField()
    numa_info = CharField()

    def create(self, validated_data):
        return EnvironmentMetadata(**validated_data)