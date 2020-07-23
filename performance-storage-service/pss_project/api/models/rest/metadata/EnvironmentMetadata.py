class EnvironmentMetadata(object):
    def __init__(self, os_version=None, cpu_number=None, numa_info=None):
        self.os_version = os_version
        self.cpu_number = cpu_number
        self.numa_info = numa_info
