from collections import namedtuple
from django.test import SimpleTestCase, TestCase
from unittest import mock

from pss_project.api.github_integration.PerformanceGuardBot import (PerformanceGuardBot, get_performance_comparisons,
                                                                    get_min_performance_change,
                                                                    generate_performance_result_markdown)
from pss_project.api.github_integration.BasePRBot import (CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL, CONCLUSION_FAILURE)
from pss_project.api.tests.factories.database.OLTPBenchDBFactory import OLTPBenchDBFactory
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult, PERFORMANCE_CONFIG_FIELDS
from pss_project.api.constants import MASTER_BRANCH_NAME

TestIteration = namedtuple('TestCase', 'input expected')


class TestPerformanceGuardBot(SimpleTestCase):

    def setUp(self):
        self.perf_bot = PerformanceGuardBot(1, 'abc', 'secret', 'name')

    @mock.patch('pss_project.api.github_integration.PerformanceGuardBot.get_performance_comparisons')
    def test_get_conclusion_data(self, mock_get_performance_comparisons):
        """ Test that get_conclusion_data returns the conclusion data if there
        is a commit sha
        """
        expected = 'data'
        mock_get_performance_comparisons.return_value = expected
        payload = {'commit': {'sha': 'hash'}}
        result = self.perf_bot.get_conclusion_data(payload)
        self.assertEqual(result, expected)

    def test_get_conclusion_data_missing_commit(self):
        """ Test that get_conclusion_data returns None if there is no commit sha
        """
        payload = {}
        result = self.perf_bot.get_conclusion_data(payload)
        self.assertEqual(result, None)

    def test_get_conclusion(self):
        """ Test that get_conclusion returns the right conclusion based on the min performance decrease passed in.
        """
        test_cases = [
            TestIteration(-5.1, CONCLUSION_FAILURE),
            TestIteration(-5, CONCLUSION_NEUTRAL),
            TestIteration(-.01, CONCLUSION_NEUTRAL),
            TestIteration(0, CONCLUSION_SUCCESS),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'a performance comparison with a min_performance_change of {input} should result'
                              f' in a check run conclusion of {expected}'):
                with mock.patch('pss_project.api.github_integration.PerformanceGuardBot.get_min_performance_change',
                                return_value=input):
                    result = self.perf_bot.get_conclusion({})
                    self.assertEqual(result, expected)

    @mock.patch('pss_project.api.github_integration.PerformanceGuardBot.generate_performance_result_markdown')
    def test_generate_conclusion_markdown(self, mock_generate_performance_result_markdown):
        """ Test that the generate_conclusion_markdown is implemented and calls generate_performance_result_markdown.
        """
        self.perf_bot.generate_conclusion_markdown({})
        mock_generate_performance_result_markdown.assert_called_once()

    def test_get_min_performance_change(self):
        """ Test that get_min_performance_change correctly calculates the min performance change based on the
        performance comparisons.
        """
        test_cases = [
            TestIteration([({}, 10, 1000, 1000), ({}, 10, 1000, 1000), ({}, 10, 1000, 1000)], 0),
            TestIteration([({}, 10, 1000, 1000), ({}, 0, 1000, 1000), ({}, 5, 1000, 1000)], 0),
            TestIteration([({}, 10, 1000, 1000), ({}, 0, 1000, 1000), ({}, -5, 1000, 1000)], -5),
            TestIteration([({}, 10, 1000, 1000), ({}, 0, 1000, 1000), ({}, -10, 1000, 1000)], -10)
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'Performance comparisons of {input} should have a min performance change of'
                              f' {expected}'):
                result = get_min_performance_change(input)
                self.assertEqual(result, expected)


class TestPerformanceGuardBotIntegration(TestCase):

    def setUp(self):
        """ Create three records for the master branch and the PR branch with the same test configs. """
        for fake_commit_id in range(0, 3):
            master_result = OLTPBenchDBFactory(git_branch=MASTER_BRANCH_NAME, git_commit_id=fake_commit_id)
            test_config = master_result.get_test_config()
            test_config['git_branch'] = 'PR'
            test_config['git_commit_id'] = fake_commit_id
            branch_result = OLTPBenchDBFactory(**test_config)
            for field in PERFORMANCE_CONFIG_FIELDS:
                setattr(branch_result, field, getattr(master_result, field))

    def test_get_performance_comparisons(self):
        """ Test that the performance comparison is generated for all the matching test configs between two
        branches.
        """
        results = get_performance_comparisons(MASTER_BRANCH_NAME, 'PR')
        for config, throughput in results:
            master_results = OLTPBenchResult.objects.get(**config, git_branch=MASTER_BRANCH_NAME)
            pr_results = OLTPBenchResult.objects.get(**config, git_branch='PR')
            master_throughput = float(master_results.metrics.get('throughput', 0))
            pr_throughput = float(pr_results.metrics.get('throughput', 0))
            expected = (pr_throughput - master_throughput) / master_throughput * 100
            self.assertEqual(throughput, expected)

    def test_generate_performance_result_markdown(self):
        """ Test that the config elements and values are represented in the markdown table
        """
        input = [({"column": 5}, 5.1234, 104, 140), ({"column": 2}, 5.1234, 789, 879)]
        result = generate_performance_result_markdown(input)
        for config, percent_diff, master_throughput, commit_throughput in input:
            for key, value in config.items():
                self.assertRegex(result, rf'|\s+{key}\s+|')
                self.assertRegex(result, rf'|\s+{value}\s+|')
            self.assertRegex(result, r'|\s+tps\(% change\)\s+|')
            self.assertRegex(result, rf'|\s+{round(percent_diff,2)}\s+|')
            self.assertRegex(result, r'|\s+master tps\s+|')
            self.assertRegex(result, rf'|\s+{round(master_throughput,2)}\s+|')
            self.assertRegex(result, r'|\s+commit tps\s+|')
            self.assertRegex(result, rf'|\s+{round(commit_throughput,2)}\s+|')
        self.assertFalse(False)
