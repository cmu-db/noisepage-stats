from rest_framework.serializers import Serializer, CharField 
from pss_project.api.models.rest.metadata.GithubMetadata import GithubMetadata

class GithubMetadataSerializer(Serializer):
    # Fields
    git_commit_id = CharField()
    git_branch = CharField()

    def create(self, validated_data):
        return GithubMetadata(**validated_data)