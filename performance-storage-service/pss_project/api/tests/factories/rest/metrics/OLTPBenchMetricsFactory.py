from factory import Factory, Faker
from pss_project.api.models.rest.metrics.OLTPBenchMetrics import OLTPBenchMetrics
from pss_project.api.tests.factories.rest.metrics.LatencyMetricsFactory import LatencyMetricsFactory
import json
from collections import OrderedDict


class OLTPBenchMetricsFactory(Factory):
    class Meta:
        model = OLTPBenchMetrics
    
    throughput = Faker('pydecimal',left_digits=9,right_digits=15, positive=True)
    latency = LatencyMetricsFactory().__dict__
    # TODO: Do we have a better way to generate an array with random length?
    incremental_metrics = [
        OrderedDict([
            ('bar', '222'),
            ('foo', '333')
        ]),
        OrderedDict([
            ('bar', '333'),
            ('foo', '444')
        ]),
        OrderedDict([
            ('bar', '333'),
            ('foo', '444'),
            ('boo', OrderedDict([
                ('aaa', '111'),
                ('bbb', '222')
            ]))
        ])
    ]