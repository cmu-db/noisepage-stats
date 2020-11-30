from django.test import TestCase

from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult
from pss_project.api.tests.factories.database.OLTPBenchDBFactory import OLTPBenchDBFactory


class TestOLTPBenchResult(TestCase):

    def test_get_test_config(self):
        oltpbench_result = OLTPBenchDBFactory()
        result = oltpbench_result.get_test_config()
        for key, value in result.items():
            self.assertEqual(getattr(oltpbench_result,key),value)
    
    def test_get_oltpbench_config_query(self):
        for fake_git_commit_id in range(0,3):
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id,git_branch='master')
        oltpbench_result = OLTPBenchDBFactory(git_commit_id=0,git_branch='master')
        result = oltpbench_result.get_oltpbench_config_query('master')
        self.assertEqual(len(result),1)

    def test_is_config_match_result_true(self):
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch='master')
        master_config = master_oltpbench_result.get_test_config()
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR', **master_config)
        result = pr_oltpbench_result.is_config_match(master_oltpbench_result)
        self.assertTrue(result)

    def test_is_config_match_result_false(self):
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch='master')
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR')
        result = pr_oltpbench_result.is_config_match(master_oltpbench_result)
        self.assertFalse(result)

    def test_compare_throughput(self):
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch='master')
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR')
        result = master_oltpbench_result.compare_throughput(pr_oltpbench_result)
        master_throughput = float(master_oltpbench_result.metrics.get('throughput',0))
        pr_throughput = float(pr_oltpbench_result.metrics.get('throughput',0))
        expected = (pr_throughput - master_throughput) / master_throughput * 100
        self.assertEqual(result, expected)

    def test_compare_throughput_no_div_by_zero(self):
        master_oltpbench_result = OLTPBenchDBFactory(git_commit_id=0, git_branch='master')
        master_oltpbench_result.metrics['throughput']=0
        pr_oltpbench_result = OLTPBenchDBFactory(git_commit_id=1, git_branch='PR')
        result = master_oltpbench_result.compare_throughput(pr_oltpbench_result)
        self.assertEqual(result, 0)

    def test_get_all_branch_results(self):
        for fake_git_commit_id in range(0,3):
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id,git_branch='master')
        for fake_git_commit_id in range(3,6):
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id,git_branch='PR')
        result = OLTPBenchResult.get_all_branch_results('PR')
        self.assertEqual(len(result),3)

    def test_get_latest_branch_results(self):
        for i in range(0,3):
            fake_git_commit_id = i*2
            entry = OLTPBenchDBFactory(git_commit_id=fake_git_commit_id, git_branch='PR')
            config = entry.get_test_config()
            OLTPBenchDBFactory(git_commit_id=fake_git_commit_id+1, git_branch='PR', **config)
        result = OLTPBenchResult.get_latest_branch_results('PR')
        self.assertEqual(len(result),3)
        for pr_result in result:
            self.assertEqual(int(pr_result.git_commit_id)%2,1)

    def test_get_branch_results_by_oltpbench_configs(self):
        entry1 = OLTPBenchDBFactory(git_commit_id=0, git_branch='master')
        config1 = entry1.get_test_config()
        OLTPBenchDBFactory(git_commit_id=1, git_branch='master')
        for i in range(10,13):
            OLTPBenchDBFactory(**config1, git_commit_id=i, git_branch='master')
            OLTPBenchDBFactory(**config1, git_commit_id=i, git_branch='PR')

        master_oltpbench_results = OLTPBenchResult.objects.all()
        result = OLTPBenchResult.get_branch_results_by_oltpbench_configs('PR',master_oltpbench_results)
        self.assertEqual(len(result),1)

        

        