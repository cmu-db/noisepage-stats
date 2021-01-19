from django.test import TestCase

from pss_project.api.models.database.MicrobenchmarkResult import MicrobenchmarkResult
from pss_project.api.tests.factories.database.MicrobenchmarkDBFactory import MicrobenchmarkDBFactory


class TestMicrobenchmarkResults(TestCase):

    def test_save(self):
        microbenchmark_result = MicrobenchmarkDBFactory()
        microbenchmark_result.save()
        all_db_objects = MicrobenchmarkResult.objects.all()
        self.assertEqual(all_db_objects.count(), 1)

    def test_smudge_time_save(self):
        microbenchmark_result_1 = MicrobenchmarkDBFactory()
        microbenchmark_result_1.save()
        microbenchmark_result_2 = MicrobenchmarkDBFactory()
        microbenchmark_result_2.time = microbenchmark_result_1.time
        microbenchmark_result_2.save()
        all_db_objects = MicrobenchmarkResult.objects.all()
        self.assertEqual(all_db_objects.count(), 2)
