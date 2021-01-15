class NoisePageMetadata(object):
    """ This class is the model of the NoisePage metadata as it is represented by the HTTP API """

    def __init__(self, db_version):
        self.db_version = db_version
