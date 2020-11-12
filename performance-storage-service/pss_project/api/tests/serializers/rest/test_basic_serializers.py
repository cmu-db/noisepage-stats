from django.test import SimpleTestCase

from pss_project.api.tests.factories.rest.metadata.GithubMetadataFactory import GithubMetadataFactory
from pss_project.api.tests.factories.rest.metadata.JenkinsMetadataFactory import JenkinsMetadataFactory
from pss_project.api.tests.factories.rest.metadata.NoisePageMetadataFactory import NoisePageMetadataFactory
from pss_project.api.tests.factories.rest.metadata.MetadataFactory import MetadataFactory
from pss_project.api.tests.factories.rest.metadata.EnvironmentMetadataFactory import EnvironmentMetadataFactory
from pss_project.api.tests.factories.rest.parameters.TransactionWeightFactory import TransactionWeightFactory
from pss_project.api.tests.factories.rest.parameters.OLTPBenchParametersFactory import OLTPBenchParametersFactory
from pss_project.api.tests.factories.rest.parameters.MicrobenchmarkParametersFactory import (
    MicrobenchmarkParametersFactory)
from pss_project.api.tests.factories.rest.metrics.OLTPBenchMetricsFactory import OLTPBenchMetricsFactory
from pss_project.api.tests.factories.rest.metrics.LatencyMetricsFactory import LatencyMetricsFactory
from pss_project.api.tests.factories.rest.metrics.MemoryMetricsFactory import (
    MemoryInfoSummaryFactory, MemoryMetricsFactory, MemorySummaryMetricsFactory)
from pss_project.api.tests.factories.rest.metrics.IncrementalMetricsFactory import IncrementalMetricsFactory
from pss_project.api.tests.factories.rest.metrics.MicrobenchmarkMetricsFactory import MicrobenchmarkMetricsFactory
from pss_project.api.tests.factories.rest.OLTPBenchRestFactory import OLTPBenchRestFactory
from pss_project.api.tests.factories.rest.MicrobenchmarkRestFactory import MicrobenchmarkRestFactory

from pss_project.api.tests.factories.rest.ArtifactStatsRestFactory import ArtifactStatsRestFactory


from pss_project.api.serializers.rest.metadata.GithubMetadataSerializer import GithubMetadataSerializer
from pss_project.api.serializers.rest.metadata.JenkinsMetadataSerializer import JenkinsMetadataSerializer
from pss_project.api.serializers.rest.metadata.NoisePageMetadataSerializer import NoisePageMetadataSerializer
from pss_project.api.serializers.rest.metadata.MetadataSerializer import MetadataSerializer
from pss_project.api.serializers.rest.metadata.EnvironmentMetadataSerializer import EnvironmentMetadataSerializer
from pss_project.api.serializers.rest.parameters.TransactionWeightSerializer import TransactionWeightSerializer
from pss_project.api.serializers.rest.parameters.OLTPBenchParametersSerializer import OLTPBenchParametersSerializer
from pss_project.api.serializers.rest.parameters.MicrobenchmarkParametersSerializer import (
    MicrobenchmarkParametersSerializer)
from pss_project.api.serializers.rest.metrics.OLTPBenchMetricsSerializer import OLTPBenchMetricsSerializer
from pss_project.api.serializers.rest.metrics.MicrobenchmarkMetricsSerializer import MicrobenchmarkMetricsSerializer
from pss_project.api.serializers.rest.metrics.LatencyMetricsSerializer import LatencyMetricsSerializer
from pss_project.api.tests.factories.rest.metrics.MemoryMetricsSerializer import (
    MemoryInfoSummarySerializer, MemoryMetricsSerializer,
    MemorySummaryMetricsSerializer)
from pss_project.api.serializers.rest.metrics.IncrementalMetricsSerializer import IncrementalMetricsSerializer
from pss_project.api.serializers.rest.OLTPBenchSerializer import OLTPBenchSerializer
from pss_project.api.serializers.rest.MicrobenchmarkSerializer import MicrobenchmarkSerializer

from pss_project.api.serializers.rest.ArtifactStatsSerializer import ArtifactStatsSerializer

from pss_project.api.tests.utils.utils import generate_dict_factory


class TestBasicSerializer(SimpleTestCase):
    # list of tests in the form (test_name, class_factory, class_serializer, excluded_fields)ƒ
    serializer_test_params = [
        ('GithubMetadataSerializer', GithubMetadataFactory,
         GithubMetadataSerializer, []),
        ('JenkinsMetadataSerializer', JenkinsMetadataFactory,
         JenkinsMetadataSerializer, []),
        ('NoisePageMetadataSerializer', NoisePageMetadataFactory,
         NoisePageMetadataSerializer, []),
        ('MetadataSerializer', MetadataFactory, MetadataSerializer, []),
        ('EnvironmentMetadataSerializer', EnvironmentMetadataFactory, EnvironmentMetadataSerializer, []),

        ('TransactionWeightSerializer', TransactionWeightFactory, TransactionWeightSerializer, []),
        ('OLTPBenchParametersSerializer', OLTPBenchParametersFactory, OLTPBenchParametersSerializer, []),

        ('MicrobenchmarkParametersSerializer', MicrobenchmarkParametersFactory, MicrobenchmarkParametersSerializer, []),

        ('OLTPBenchMetricsSerializer', OLTPBenchMetricsFactory, OLTPBenchMetricsSerializer, []),
        ('LatencyMetricsSerializer', LatencyMetricsFactory, LatencyMetricsSerializer, []),
        ('MemoryInfoSummaryMetricsSerializer', MemoryInfoSummaryFactory, MemoryInfoSummaryMetricsSerializer, []),
        ('MemoryMetricsSerializer', MemoryMetricsFactory, MemoryMetricsSerializer, []),
        ('MemorySummaryMetricsSerializer', MemorySummaryMetricsFactory, MemorySummaryMetricsSerializer, []),
        ('IncrementalMetricsSerializer', IncrementalMetricsFactory, IncrementalMetricsSerializer, []),

        ('MicrobenchmarkMetricsSerializer', MicrobenchmarkMetricsFactory, MicrobenchmarkMetricsSerializer, []),

        ('OLTPBenchSerializer', OLTPBenchRestFactory, OLTPBenchSerializer, ['timestamp']),
        ('MicrobenchmarkSerializer', MicrobenchmarkRestFactory, MicrobenchmarkSerializer, ['timestamp']),
        ('ArtifactStatsSerializer', ArtifactStatsRestFactory, ArtifactStatsSerializer, ['timestamp']),
    ]

    def test_serialize_model_fields(self):
        for test_name, class_factory, class_serializer, excluded_fields in self.serializer_test_params:
            with self.subTest(
                    msg="{} serializer data fields matches the object.".format(
                        test_name)):
                input = class_factory()
                serializer = class_serializer(input)
                input_keys = list(input.__dict__.keys())
                serializer_keys = list(serializer.data.keys())
                self.assertListEqual(input_keys, serializer_keys)

    def test_deserialize_model_fields(self):
        for test_name, class_factory, class_serializer, excluded_fields in self.serializer_test_params:
            with self.subTest(
                    msg="Deserialization with {} is valid".format(test_name)):
                ClassDictFactory = generate_dict_factory(class_factory)
                input = ClassDictFactory()
                serializer = class_serializer(data=input)
                self.assertTrue(serializer.is_valid(), msg=serializer.errors)
