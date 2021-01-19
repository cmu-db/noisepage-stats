from django.test import TestCase

from pss_project.api.models.database.ArtifactStatsResult import ArtifactStatsResult
from pss_project.api.tests.factories.database.ArtifactStatsDBFactory import ArtifactStatsDBFactory


class TestArtifactStatsResults(TestCase):

    def test_save(self):
        artifact_stats_result = ArtifactStatsDBFactory()
        artifact_stats_result.save()
        all_db_objects = ArtifactStatsResult.objects.all()
        self.assertEqual(all_db_objects.count(), 1)

    def test_smudge_time_save(self):
        artifact_stats_result_1 = ArtifactStatsDBFactory()
        artifact_stats_result_1.save()
        artifact_stats_result_2 = ArtifactStatsDBFactory()
        artifact_stats_result_2.time = artifact_stats_result_1.time
        artifact_stats_result_2.save()
        all_db_objects = ArtifactStatsResult.objects.all()
        self.assertEqual(all_db_objects.count(), 2)
