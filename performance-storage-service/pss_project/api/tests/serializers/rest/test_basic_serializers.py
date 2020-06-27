from django.test import SimpleTestCase

from pss_project.api.tests.factories.rest.metadata.GithubMetadataFactory import GithubMetadataFactory
from pss_project.api.tests.factories.rest.metadata.JenkinsMetadataFactory import JenkinsMetadataFactory
from pss_project.api.tests.factories.rest.metadata.NoisePageMetadataFactory import NoisePageMetadataFactory
from pss_project.api.tests.factories.rest.metadata.OLTPBenchMetadataFactory import OLTPBenchMetadataFactory
from pss_project.api.tests.factories.rest.parameters.TransactionWeightFactory import TransactionWeightFactory
from pss_project.api.tests.factories.rest.parameters.OLTPBenchParameters import OLTPBenchParametersFactory
from pss_project.api.tests.factories.rest.metrics.OLTPBenchMetricsFactory import OLTPBenchMetricsFactory
from pss_project.api.tests.factories.rest.metrics.LatencyMetricsFactory import LatencyMetricsFactory
from pss_project.api.tests.factories.rest.OLTPBenchRestFactory import OLTPBenchRestFactory

from pss_project.api.serializers.rest.metadata.GithubMetadataSerializer import GithubMetadataSerializer
from pss_project.api.serializers.rest.metadata.JenkinsMetadataSerializer import JenkinsMetadataSerializer
from pss_project.api.serializers.rest.metadata.NoisePageMetadataSerializer import NoisePageMetadataSerializer
from pss_project.api.serializers.rest.metadata.OLTPBenchMetadataSerializer import OLTPBenchMetadataSerializer
from pss_project.api.serializers.rest.parameters.TransactionWeightSerializer import TransactionWeightSerializer
from pss_project.api.serializers.rest.parameters.OLTPBenchParametersSerializer import OLTPBenchParametersSerializer
from pss_project.api.serializers.rest.metrics.OLTPBenchMetricsSerializer import OLTPBenchMetricsSerializer
from pss_project.api.serializers.rest.metrics.LatencyMetricsSerializer import LatencyMetricsSerializer
from pss_project.api.serializers.rest.OLTPBenchSerializer \
    import OLTPBenchSerializer

from pss_project.api.tests.utils.utils import generate_dict_factory


class TestBasicSerializer(SimpleTestCase):
    # list of tests in the form (test_name, class_factory, class_serializer, excluded_fields)ƒ
    serializer_test_params = [
        ('GithubMetadataSerializer', GithubMetadataFactory, GithubMetadataSerializer, []),
        ('JenkinsMetadataSerializer',JenkinsMetadataFactory,JenkinsMetadataSerializer, []),
        ('NoisePageMetadataSerializer',NoisePageMetadataFactory,NoisePageMetadataSerializer, []),
        ('OLTPBenchMetadataSerializer',OLTPBenchMetadataFactory,OLTPBenchMetadataSerializer, []),
        ('TransactionWeightSerializer',TransactionWeightFactory,TransactionWeightSerializer, []),
        ('OLTPBenchParametersSerializer',OLTPBenchParametersFactory,OLTPBenchParametersSerializer, []),
        ('OLTPBenchMetricsSerializer',OLTPBenchMetricsFactory,OLTPBenchMetricsSerializer, []),
        ('LatencyMetricsSerializer',LatencyMetricsFactory,LatencyMetricsSerializer,[]),
        ('OLTPBenchSerializer',OLTPBenchRestFactory,OLTPBenchSerializer,['timestamp']),
    ]

    def test_serialize_model_fields(self):
        for test_name, class_factory, class_serializer, excluded_fields in self.serializer_test_params:
            with self.subTest(msg="{} serializer data fields matches the object.".format(test_name)):
                input = class_factory()
                serializer = class_serializer(input)
                self.assertListEqual(list(input.__dict__.keys()), list(serializer.data.keys()))

    def test_deserialize_model_fields(self):
        for test_name, class_factory, class_serializer, excluded_fields in self.serializer_test_params:
            with self.subTest(msg="Deserialization with {} is valid".format(test_name)):
                ClassDictFactory = generate_dict_factory(class_factory)
                input = ClassDictFactory()
                serializer = class_serializer(data=input)
                self.assertTrue(serializer.is_valid(),msg=serializer.errors)
