from rest_framework.serializers import Serializer, CharField, ChoiceField
from pss_project.api.models.rest.metadata.EnvironmentMetadata import EnvironmentMetadata


class EnvironmentMetadataSerializer(Serializer):
    # Constants
    RAM_DISK = 'RAM disk'
    HDD = 'HDD'
    SATA_SSD = 'SATA SSD'
    NVME_SSD = 'NVMe SSD'
    NONE = 'None'
    WAL_DEVICE_CHOICES = [
        (RAM_DISK, 'RAM disk'),
        (HDD, 'HDD'),
        (SATA_SSD, 'SATA SSD'),
        (NVME_SSD, 'NVMe SSD'),
        (NONE, 'None')
    ]
    # Fields
    os_version = CharField()
    cpu_number = CharField()
    cpu_socket = CharField()
    wal_device = ChoiceField(choices=WAL_DEVICE_CHOICES)

    def create(self, validated_data):
        return EnvironmentMetadata(**validated_data)
