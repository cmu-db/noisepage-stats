from collections import namedtuple
from django.test import SimpleTestCase
from unittest import mock

from pss_project.api.github_integration.BasePRBot import BasePRBot
from pss_project.api.constants import CI_STATUS_CONTEXT


TestIteration = namedtuple('TestCase', 'input expected')


class TestBasePRBot(SimpleTestCase):

    @mock.patch('pss_project.api.github_integration.NoisePageRepoClient.NoisePageRepoClient')
    def setUp(self, mock_repo_client):
        self.bot = BasePRBot(mock_repo_client(), 'name')

    def test_handle_initialize_event_invalid_event(self):
        """ Test that if an event other than the initialize even occurs then
        nothing will happen """
        mock_bot = mock.Mock(wraps=self.bot)
        payload = {}
        mock_bot.handle_initialize_event('bad-event', payload)
        self.assertEqual(mock_bot.should_initialize_check_run.call_count, 0)

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
                self.setUp()
                result = self.bot.should_initialize_check_run(input)
                self.assertEqual(result, expected)

    def test_initialize_check_run(self):
        """ Test that this calls the repo client to create a check run """
        commit_sha = '123qwer567'

        self.bot.initialize_check_run({'commit': {'sha': commit_sha}})
        self.bot.repo_client.create_check_run.assert_called_once()

    def test_create_initial_check_run(self):
        """ Test that this properly uses the class attributes to create the
        initial check body """
        commit_sha = '123qwer567'
        result = self.bot.create_initial_check_run(commit_sha)
        self.assertEqual(self.bot.initialize_title, result.get('output').get('title'))
        self.assertEqual(self.bot.initialize_summary, result.get('output').get('summary'))
        self.assertEqual(commit_sha, result.get('head_sha'))

    def test_handle_completion_event_invalid_event(self):
        """ Test that if an event other than the completion even occurs then
        nothing will happen """
        mock_bot = mock.Mock(wraps=self.bot)
        payload = {}
        mock_bot.handle_completion_event('bad-event', payload)
        self.assertEqual(mock_bot.should_complete_check_run.call_count, 0)

    def test_should_complete_check_run(self):
        with mock.patch.object(self.bot, 'is_ci_complete'):
            payload = {'commit': {'sha': 'hash'}}
            self.bot.should_complete_check_run(payload)
            self.bot.is_ci_complete.assert_called_once()

    def test_should_complete_check_run_missing_commit(self):
        """ Test that if there is no commit hash in the payload then the check
        should not be completed. """
        payload = {}
        result = self.bot.should_complete_check_run(payload)
        self.assertFalse(result)

    def test_is_ci_complete(self):
        """ Test that the it can determine if the ci is complete based on the
        commit status"""
        test_cases = [
            TestIteration({'statuses': [{'context': CI_STATUS_CONTEXT, 'state': 'success'}]}, True),
            TestIteration({'statuses': []}, False),
            TestIteration({}, False),
            TestIteration({'statuses': [{'context': CI_STATUS_CONTEXT, 'state': 'failed'}]}, False),
        ]

        for input, expected in test_cases:
            with self.subTest(msg=f'on get_commit_status response of {input} is_ci_complete should return {expected}'):
                self.setUp()
                self.bot.repo_client.get_commit_status.return_value = input

                result = self.bot.is_ci_complete('hash')
                self.assertEqual(result, expected)

    def test_complete_check_run_missing_commit(self):
        mock.Mock(wraps=self.bot)
        payload = {}
        self.bot.complete_check_run(payload)
        self.bot.repo_client.get_commit_check_run_for_app.assert_not_called()

    def test_complete_check_run(self):
        test_cases = [
            TestIteration({'id': 'hey'}, 1),
            TestIteration(None, 0),
        ]

        for input, expected in test_cases:
            with self.subTest(msg=f'on get_commit_check_run_for_app response of {input} then create_complete_check_run'
                              f' is called {expected} times.'):
                self.setUp()
                self.bot.repo_client.get_commit_check_run_for_app.return_value = input
                mock.Mock(wraps=self.bot)
                complete_check_body = {}
                self.bot.create_complete_check_run = mock.Mock(side_effect=lambda x: complete_check_body)

                payload = {'commit': {'sha': 'hash'}}
                self.bot.complete_check_run(payload)
                self.assertEqual(self.bot.create_complete_check_run.call_count, expected)
                if expected > 0:
                    self.bot.repo_client.update_check_run.assert_called_with(input.get('id'), complete_check_body)

    def test_create_complete_check_run(self):
        conclusion = 'success'
        title = 'title'
        summary = 'summary'
        text = 'text'
        self.bot.conclusion_title_map = {
            conclusion: title
        }
        self.bot.conclusion_summary_map = {
            conclusion: summary
        }

        self.bot.get_conclusion_data = mock.Mock(side_effect=lambda x: 'data')
        self.bot.get_conclusion = mock.Mock(side_effect=lambda x: conclusion)
        self.bot.generate_conclusion_markdown = mock.Mock(side_effect=lambda x: text)
        payload = {}
        result = self.bot.create_complete_check_run(payload)
        self.assertEqual(result.get('name'), self.bot.name)
        self.assertEqual(result.get('status'), 'completed')
        self.assertEqual(result.get('conclusion'), conclusion)
        self.assertEqual(result.get('output').get('title'), title)
        self.assertEqual(result.get('output').get('summary'), summary)
        self.assertEqual(result.get('output').get('text'), text)

    def test_should_reinitialize_check_run(self):
        test_cases = [
            TestIteration(({}, None), False),
            TestIteration(({'status': 'success', 'commit': {'sha': 'hash'}},
                           {'statuses': [], 'state':'failed'}), False),
            TestIteration(({'status': 'success', 'commit': {'sha': 'hash'}},
                           {'statuses': [{'context': CI_STATUS_CONTEXT}], 'state': 'success'}), False),
            TestIteration(({'status': 'success', 'commit': {'sha': 'hash'}},
                           {'statuses': [{'context': CI_STATUS_CONTEXT}], 'state': 'failed'}), True),
        ]
        for input, expected in test_cases:
            (payload, get_commit_status_response) = input
            with self.subTest(msg=f'on payload of {payload} and get_commit_status_reponse of'
                              f' {get_commit_status_response} return {expected}'):
                self.setUp()
                self.bot.repo_client.get_commit_status.return_value = get_commit_status_response

                result = self.bot.should_reinitialize_check_run(payload)
                self.assertEqual(result, expected)

    def test_initialize_check_run_if_missing(self):
        """ Test that the check run will be initialized if repo_client reports
        that it is missing. Don't initialize otherwise """
        test_cases = [
            TestIteration({"check_runs": [{"name": self.bot.name}]}, 0),
            TestIteration({"check_runs": [{"name": "wrong name"}]}, 1),
            TestIteration(None, 1)
        ]
        for get_commit_check_run_for_app_return_value, expected_create_check_run_call_count in test_cases:
            with self.subTest(msg=(f'If github client returns {get_commit_check_run_for_app_return_value} then'
                                   f' create_check_run should be called {expected_create_check_run_call_count} times')):
                self.setUp()
                commit_sha = '123qwer567'
                self.bot.repo_client.get_commit_check_run_for_app.return_value = get_commit_check_run_for_app_return_value

                self.bot.initialize_check_run_if_missing({'commit': {'sha': commit_sha}})
                self.assertEqual(self.bot.repo_client.create_check_run.call_count,
                                 expected_create_check_run_call_count)
