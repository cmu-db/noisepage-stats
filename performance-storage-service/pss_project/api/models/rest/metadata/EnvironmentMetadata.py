class EnvironmentMetadata(object):
    def __init__(self, os_version=None, cpu_number=None, cpu_socket=None, wal_device=None):
        self.os_version = os_version
        self.cpu_number = cpu_number
        self.cpu_socket = cpu_socket
        self.wal_device = wal_device
