from collections import namedtuple
from django.test import SimpleTestCase, TestCase
from unittest import skip, mock

from pss_project.api.github_integration.check_run import (
    should_initialize_check_run, initialize_check_run_if_missing, initialize_check_run, get_comparisons_conclusion, 
    get_performance_comparisons_conclusion, get_performance_comparisons, cleanup_check_run, 
    generate_performance_result_markdown, CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL, CONCLUSION_FAILURE)
from pss_project.api.tests.factories.database.OLTPBenchDBFactory import OLTPBenchDBFactory
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult, PERFORMANCE_CONFIG_FIELDS
from pss_project.api.github_integration.NoisePageRepoClient import NoisePageRepoClient

TestIteration = namedtuple('TestCase', 'input expected')


class TestCheckRun(SimpleTestCase):

    def test_should_initialize_check_run(self):
        """ Test that some pull request events trigger initializing a check run while others do not """
        test_cases = [
            TestIteration('synchronize', True),
            TestIteration('opened', True),
            TestIteration('reopened', True),
            TestIteration('closed', False),
            TestIteration('merged', False),
        ]

        for input, expected in test_cases:
            with self.subTest(msg=f'on {input} pull request should_initialize_check_run should return {expected}'):
                result = should_initialize_check_run(input)
                self.assertEqual(result, expected)

    @mock.patch('pss_project.api.github_integration.NoisePageRepoClient.NoisePageRepoClient')
    def test_initialize_check_run_if_missing(self, mock_repo_client):
        test_cases = [
            TestIteration({"check_run":"valid"}, 0),
            TestIteration(None,1)
        ]
        for get_commit_check_run_for_app_return_value, create_check_run_call_count in test_cases:
            with self.subTest(msg=(f'If github client returns {get_commit_check_run_for_app_return_value} then' 
                                    f' create_check_run should be called {create_check_run_call_count} times')):
                repo_client = mock_repo_client()
                commit_sha = '123qwer567'
                repo_client.get_commit_check_run_for_app.return_value = get_commit_check_run_for_app_return_value
                initialize_check_run_if_missing(repo_client, commit_sha)
                self.assertEqual(create_check_run_call_count, repo_client.create_check_run.call_count)
    
    @mock.patch('pss_project.api.github_integration.NoisePageRepoClient.NoisePageRepoClient')
    def test_initialize_check_run(self, mock_repo_client):
        repo_client = mock_repo_client()
        commit_sha = '123qwer567'
        initialize_check_run(repo_client, commit_sha)
        repo_client.create_check_run.assert_called_once()
        

    def test_get_comparisons_conclusion(self):
        """ Test the correct conclusion is reached based on the min throughput input """
        test_cases = [
            TestIteration(-5.1, CONCLUSION_FAILURE),
            TestIteration(-5, CONCLUSION_NEUTRAL),
            TestIteration(-.01, CONCLUSION_NEUTRAL),
            TestIteration(0, CONCLUSION_SUCCESS),
        ]

        for input, expected in test_cases:
            with self.subTest(msg=(f'a performance comparison with a min_performance_change of {input} should result in'
                                   ' a check run conclusion of {expected}')):
                result = get_comparisons_conclusion(input)
                self.assertEqual(result, expected)

    def test_get_performance_comparisons_conclusion(self):
        """ Test that the conclusion is based on the min throughput number for a set of comparisons """
        test_cases = [
            TestIteration([({}, 10), ({}, 0), ({}, 5)], CONCLUSION_SUCCESS),
            TestIteration([({}, 10), ({}, 0), ({}, -5)], CONCLUSION_NEUTRAL),
            TestIteration([({}, 10), ({}, 0), ({}, -10)], CONCLUSION_FAILURE)
        ]
        for input, expected in test_cases:
            with self.subTest(msg=(f'performance comparison expected {expected} check run conclusion')):
                result = get_performance_comparisons_conclusion(input)
                self.assertEqual(result, expected)


class TestCheckRunIntegration(TestCase):
    def setUp(self):
        """ Create three records for the master branch and the PR branch with the same test configs. """
        for fake_commit_id in range(0, 3):
            master_result = OLTPBenchDBFactory(git_branch='master', git_commit_id=fake_commit_id)
            test_config = master_result.get_test_config()
            test_config['git_branch'] = 'PR'
            test_config['git_commit_id'] = fake_commit_id
            branch_result = OLTPBenchDBFactory(**test_config)
            for field in PERFORMANCE_CONFIG_FIELDS:
                setattr(branch_result, field, getattr(master_result, field))

    def test_get_performance_comparisons(self):
        """ Test that the performance comparison is generated for all the matching test configs between two 
        branches. """
        results = get_performance_comparisons('master', 'PR')
        for config, throughput in results:
            master_results = OLTPBenchResult.objects.get(**config, git_branch='master')
            pr_results = OLTPBenchResult.objects.get(**config, git_branch='PR')
            master_throughput = float(master_results.metrics.get('throughput', 0))
            pr_throughput = float(pr_results.metrics.get('throughput', 0))
            expected = (pr_throughput - master_throughput) / master_throughput * 100
            self.assertEqual(throughput, expected)

    def test_generate_performance_result_markdown(self):
        """ Test that the config elements and values are represented in the markdown table """
        input = [({"column": 5}, 5.1234), ({"column": 2}, 5.1234)]
        result = generate_performance_result_markdown(input)
        for config, percent_diff in input:
            for key, value in config.items():
                self.assertRegex(result, rf'|\s+{key}\s+|')
                self.assertRegex(result, rf'|\s+{value}\s+|')
            self.assertRegex(result, r'|\s+tps\(% change\)\s+|')
            self.assertRegex(result, rf'|\s+{round(percent_diff,2)}\s+|')
        self.assertFalse(False)

    @skip("Skipping until the real implementation is live")
    def test_cleanup_check_run(self):
        """ Test that the cleanup will delete all records for a specific branch """
        cleanup_check_run('PR')
        master_results = OLTPBenchResult.objects.filter(git_branch='master')
        pr_results = OLTPBenchResult.objects.filter(git_branch='PR')
        self.assertEqual(len(pr_results), 0)
        self.assertGreater(len(master_results), 0)
