from rest_framework.serializers import Serializer, CharField
from pss_project.api.models.rest.metadata.NoisePageMetadata import NoisePageMetadata


class NoisePageMetadataSerializer(Serializer):
    # Fields
    version = CharField()

    def create(self, validated_data):
        return NoisePageMetadata(**validated_data)
