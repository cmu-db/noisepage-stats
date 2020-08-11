from rest_framework.serializers import Serializer, ChoiceField, DecimalField, IntegerField
from pss_project.api.serializers.rest.parameters.TransactionWeightSerializer import TransactionWeightSerializer
from pss_project.api.models.rest.parameters.OLTPBenchParameters import OLTPBenchParameters


class OLTPBenchParametersSerializer(Serializer):
    # Constants
    SIMPLE_MODE = 'simple'
    EXTENDED_MODE = 'extended'
    QUERY_MODE_CHOICES = [
        (SIMPLE_MODE, 'simple'),
        (EXTENDED_MODE, 'extended'),
    ]
    RAM_DISK = 'RAM disk'
    HDD = 'HDD'
    SATA_SSD = 'SATA SSD'
    NVME_SSD = 'NVMe SSD'
    WAL_DEVICE_CHOICES = [
        (RAM_DISK, 'RAM disk'),
        (HDD, 'HDD'),
        (SATA_SSD, 'SATA SSD'),
        (NVME_SSD, 'NVMe SSD')
    ]

    # Fields
    query_mode = ChoiceField(choices=QUERY_MODE_CHOICES)
    scale_factor = DecimalField(max_digits=10, decimal_places=4, coerce_to_string=False)
    terminals = IntegerField()
    client_time = IntegerField()
    transaction_weights = TransactionWeightSerializer(many=True)
    wal_device = ChoiceField(choices=WAL_DEVICE_CHOICES)
    max_connection_threads = IntegerField()

    def create(self, validated_data):
        return OLTPBenchParameters(**validated_data)
