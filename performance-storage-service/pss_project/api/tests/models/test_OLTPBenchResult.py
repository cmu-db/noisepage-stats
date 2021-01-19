from django.test import TestCase

from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult
from pss_project.api.tests.factories.database.OLTPBenchDBFactory import OLTPBenchDBFactory
from pss_project.api.constants import MASTER_BRANCH_NAME


class TestOLTPBenchResult(TestCase):

    def test_save(self):
        oltpbench_result = OLTPBenchDBFactory()
        oltpbench_result.save()
        all_db_objects = OLTPBenchResult.objects.all()
        self.assertEqual(len(all_db_objects), 1)

    def test_smudge_time_save(self):
        oltpbench_result_1 = OLTPBenchDBFactory()
        oltpbench_result_1.save()
        oltpbench_result_2 = OLTPBenchDBFactory()
        oltpbench_result_2.time = oltpbench_result_1.time
        oltpbench_result_2.save()
        all_db_objects = OLTPBenchResult.objects.all()
        self.assertEqual(len(all_db_objects), 2)

    def test_get_test_config(self):
        """ Test that the config settings are returned"""
        oltpbench_result = OLTPBenchDBFactory()
        result = oltpbench_result.get_test_config()
        for key, value in result.items():
            self.assertEqual(getattr(oltpbench_result, key), value)

    def test_get_oltpbench_config_query(self):
        """ Test that a query set is generated to query based on a provided config and branch"""
        for fake_git_commit_id in range(0, 3):
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id, git_branch=MASTER_BRANCH_NAME)
        oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch=MASTER_BRANCH_NAME)
        result = oltpbench_result.get_oltpbench_config_query(MASTER_BRANCH_NAME)
        self.assertEqual(len(result), 1)

    def test_is_config_match_result_true(self):
        """ Test that it returns true if two configs match """
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch=MASTER_BRANCH_NAME)
        master_config = master_oltpbench_result.get_test_config()
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR', **master_config)
        result = pr_oltpbench_result.is_config_match(master_oltpbench_result)
        self.assertTrue(result)

    def test_is_config_match_result_false(self):
        """ Test that it returns false if two configs do not match """
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch=MASTER_BRANCH_NAME)
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR')
        result = pr_oltpbench_result.is_config_match(master_oltpbench_result)
        self.assertFalse(result)

    def test_compare_throughput(self):
        """ Test that the throughputs of two results can be compared and genereate a percent difference """
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch=MASTER_BRANCH_NAME)
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR')
        result = master_oltpbench_result.compare_throughput(pr_oltpbench_result)
        master_throughput = float(master_oltpbench_result.metrics.get('throughput', 0))
        pr_throughput = float(pr_oltpbench_result.metrics.get('throughput', 0))
        expected = (pr_throughput - master_throughput) / master_throughput * 100
        self.assertEqual(result, expected)

    def test_compare_throughput_no_div_by_zero(self):
        """ Test that the function returns 0 instead of hitting a divide by 0 error """
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch=MASTER_BRANCH_NAME)
        master_oltpbench_result.metrics['throughput'] = 0
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR')
        result = master_oltpbench_result.compare_throughput(pr_oltpbench_result)
        self.assertEqual(result, 0)

    def test_get_all_branch_results(self):
        """ Test that a query set is generated only containing results for that branch """
        for fake_git_commit_id in range(0, 3):
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id, git_branch=MASTER_BRANCH_NAME)
        for fake_git_commit_id in range(3, 6):
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id, git_branch='PR')
        result = OLTPBenchResult.get_all_branch_results('PR')
        self.assertEqual(len(result), 3)

    def test_get_latest_commit_results(self):
        """ Test that a query set is generated that returns the latest result for each distinct config """
        entry = OLTPBenchDBFactory(git_commit_id=0, git_branch='PR')
        config = entry.get_test_config()
        OLTPBenchDBFactory(git_commit_id=1, git_branch='PR', **config)
        result = OLTPBenchResult.get_latest_commit_results(1)
        self.assertEqual(len(result), 1)
        for pr_result in result:
            self.assertEqual(int(pr_result.git_commit_id), 1)

    def test_get_branch_results_by_oltpbench_configs(self):
        """ Test that a query set is generated that returns the latest result for each config passed in as
        oltpbench_results"""
        entry1 = OLTPBenchDBFactory(git_commit_id=0, git_branch=MASTER_BRANCH_NAME)
        config1 = entry1.get_test_config()
        OLTPBenchDBFactory(git_commit_id=1, git_branch=MASTER_BRANCH_NAME)
        for i in range(10, 13):
            OLTPBenchDBFactory(**config1, git_commit_id=i, git_branch=MASTER_BRANCH_NAME)
            OLTPBenchDBFactory(**config1, git_commit_id=i, git_branch='PR')

        master_oltpbench_results = OLTPBenchResult.objects.all()
        result = OLTPBenchResult.get_branch_results_by_oltpbench_configs('PR', master_oltpbench_results)
        self.assertEqual(len(result), 1)
