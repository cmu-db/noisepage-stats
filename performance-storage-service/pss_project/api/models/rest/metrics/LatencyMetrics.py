class LatencyMetrics(object):
    def __init__(self, l_25=None, l_75=None, l_90=None, l_95=None, l_99=None, avg=None, median=None, max=None, min=None):
        if l_25:
            self.l_25 = l_25
        if l_75:
            self.l_75 = l_75
        if l_90:
            self.l_90 = l_90
        if l_95:
            self.l_95 = l_95 
        if l_99:
            self.l_99 = l_99 
        if avg:
            self.avg = avg
        if median:
            self.median = median
        if max:
            self.max = max
        if min:
            self.min = min