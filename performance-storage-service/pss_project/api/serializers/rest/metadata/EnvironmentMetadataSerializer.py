from rest_framework.serializers import Serializer, CharField, ChoiceField
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata
from pss_project.api.constants import WAL_DEVICE_CHOICES


class EnvironmentMetadataSerializer(Serializer):
    # Fields
    os_version = CharField()
    cpu_number = CharField()
    cpu_socket = CharField()
    wal_device = ChoiceField(choices=WAL_DEVICE_CHOICES)

    def create(self, validated_data):
        return EnvironmentMetadata(**validated_data)
