class LatencyMetrics(object):
    def __init__(self, l_25=None, l_75=None, l_90=None, l_95=None, l_99=None, avg=None, median=None, max=None, min=None):
        self.l_25 = l_25
        self.l_75 = l_75
        self.l_90 = l_90
        self.l_95 = l_95 
        self.l_99 = l_99 
        self.avg = avg
        self.median = median
        self.max = max
        self.min = min