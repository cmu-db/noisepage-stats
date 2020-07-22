from rest_framework.serializers import Serializer, CharField, IntegerField
from pss_project.api.models.rest.parameters.TransactionWeight import TransactionWeight


class TransactionWeightSerializer(Serializer):
    # Fields
    name = CharField()
    weight = IntegerField()

    def create(self, validated_data):
        return TransactionWeight(**validated_data)
