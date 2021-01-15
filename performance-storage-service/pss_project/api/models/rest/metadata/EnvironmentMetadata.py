class EnvironmentMetadata(object):
    """ This class is the model of the environment data relating to the system that the tests/metrics were collected
    on. This class is how the model is represented in the HTTP API """

    def __init__(self, os_version=None, cpu_number=None, cpu_socket=None, wal_device=None):
        self.os_version = os_version
        self.cpu_number = cpu_number
        self.cpu_socket = cpu_socket
        self.wal_device = wal_device
