from rest_framework.serializers import Serializer, CharField
from pss_project.api.models.rest.metadata.GithubMetadata import GithubMetadata


class GithubMetadataSerializer(Serializer):
    # Fields
    commit_id = CharField()
    branch = CharField()

    def create(self, validated_data):
        return GithubMetadata(**validated_data)
