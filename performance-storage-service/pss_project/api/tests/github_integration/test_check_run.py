from collections import namedtuple
from django.test import SimpleTestCase, TestCase
from unittest import skip

from pss_project.api.github_integration.check_run import (
    should_initialize_check_run, get_comparisons_conclusion, get_performance_comparisons_conclusion, 
    get_performance_comparisons, cleanup_check_run, CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL, CONCLUSION_FAILURE)
from pss_project.api.tests.factories.database.OLTPBenchDBFactory import OLTPBenchDBFactory
from pss_project.api.models.database.OLTPBenchResult import OLTPBenchResult, PERFORMANCE_CONFIG_FIELDS

TestIteration = namedtuple('TestCase', 'input expected')


class TestCheckRun(SimpleTestCase):

    def test_should_initialize_check_run(self):
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

    def test_get_comparisons_conclusion(self):
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
        for fake_commit_id in range(0,3):
            master_result = OLTPBenchDBFactory(git_branch='master',git_commit_id=fake_commit_id)
            test_config = master_result.get_test_config()
            test_config['git_branch'] = 'PR'
            test_config['git_commit_id'] = fake_commit_id
            branch_result = OLTPBenchDBFactory(**test_config)
            for field in PERFORMANCE_CONFIG_FIELDS:
                setattr(branch_result,field, getattr(master_result,field))

    def test_get_performance_comparisons(self):
        results = get_performance_comparisons('master','PR')
        for config, throughput in results:
            master_results = OLTPBenchResult.objects.get(**config,git_branch='master')
            pr_results = OLTPBenchResult.objects.get(**config,git_branch='PR')
            master_throughput = float(master_results.metrics.get('throughput', 0))
            pr_throughput = float(pr_results.metrics.get('throughput', 0))
            expected = (pr_throughput - master_throughput) / master_throughput * 100
            self.assertEqual(throughput, expected)

    @skip("Skipping until the real implementation is live")
    def test_cleanup_check_run(self):
        cleanup_check_run('PR')
        master_results = OLTPBenchResult.objects.filter(git_branch='master')
        pr_results = OLTPBenchResult.objects.filter(git_branch='PR')
        self.assertEqual(len(pr_results),0)
        self.assertGreater(len(master_results),0)
            
