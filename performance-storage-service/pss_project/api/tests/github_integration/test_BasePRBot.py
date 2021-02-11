from collections import namedtuple
from django.test import SimpleTestCase
from unittest.mock import patch, Mock, ANY

from pss_project.api.github_integration.BasePRBot import BasePRBot
from pss_project.api.constants import CI_STATUS_CONTEXT


TestIteration = namedtuple('TestCase', 'input expected')


class TestBasePRBot(SimpleTestCase):

    @patch('pss_project.api.github_integration.NoisePageRepoClient.NoisePageRepoClient')
    def setUp(self, mock_repo_client):
        self.bot = BasePRBot(mock_repo_client(), 'name')
        self.bot.should_add_pr_comment = False

    @patch.multiple(BasePRBot,
                    _handle_initialize_event=Mock(),
                    _handle_reinitialize_event=Mock(),
                    _handle_completion_event=Mock())
    def test_run(self):
        """ Test that the all the event handler methods are called and passed
        the event and payload. """
        event = 'nothing'
        payload = {}
        self.bot.run(event, payload)
        self.bot._handle_initialize_event.assert_called_once_with(event, payload)
        self.bot._handle_reinitialize_event.assert_called_once_with(event, payload)
        self.bot._handle_completion_event.assert_called_once_with(event, payload)

    @patch.object(BasePRBot, '_should_initialize_check_run', Mock())
    def test_handle_initialize_event_invalid_event(self):
        """ Test that if an event other than the initialize event occurs then
        nothing will happen. """
        payload = {}
        self.bot._handle_initialize_event('bad-event', payload)
        self.bot._should_initialize_check_run.assert_not_called()

    def test_handle_initialize_event(self):
        """ Test that if an event occurs where the check run should be initialized
        then it is. If it shouldn't be initialized then it is not. """
        test_cases = [
            TestIteration(True, 1),
            TestIteration(False, 0),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if _should_initialize_check_run is {input} then _initialize_check_run is called'
                              f' {expected} times.'):
                self.setUp()
                with patch.multiple(BasePRBot, _should_initialize_check_run=Mock(return_value=input),
                                    _initialize_check_run=Mock()):
                    event = self.bot.initialize_event
                    payload = {}
                    self.bot._handle_initialize_event(event, payload)
                    self.assertEqual(self.bot._initialize_check_run.call_count, expected)

    def test_get_commit_sha_from_initialize_event_payload(self):
        """ Test that the commit hash can be retrieved from the payload for
        initialization events. """
        test_cases = [
            TestIteration({self.bot.initialize_event: {'head': {'sha': 'hash'}}}, 'hash'),
            TestIteration({}, None),
            TestIteration({self.bot.initialize_event: {}}, None),
            TestIteration({self.bot.initialize_event: {'head': {}}}, None),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if payload {input} the hash returned should be {expected}'):
                result = self.bot._get_commit_sha_from_initialize_event_payload(input)
                self.assertEqual(result, expected)

    def test_should_initialize_check_run(self):
        """ Test that some pull request events trigger initializing a check run
        while others do not."""
        test_cases = [
            TestIteration({'action': 'synchronize'}, True),
            TestIteration({'action': 'opened'}, True),
            TestIteration({'action': 'reopened'}, True),
            TestIteration({'action': 'closed'}, False),
            TestIteration({'action': 'merged'}, False),
        ]

        for input, expected in test_cases:
            with self.subTest(msg=f'on {input} pull request should_initialize_check_run should return {expected}'):
                self.setUp()
                result = self.bot._should_initialize_check_run(input)
                self.assertEqual(result, expected)

    def test_initialize_check_run_missing_commit(self):
        """ Test that the check run is not initialized if the event does not
        have a commit hash. """
        payload = {}
        self.bot._initialize_check_run(payload)
        self.bot.repo_client.create_check_run.assert_not_called()

    def test_initialize_check_run(self):
        """ Test that this calls the repo client to create a check run. """
        payload = {self.bot.initialize_event: {'head': {'sha': 'hash'}}}
        self.bot._initialize_check_run(payload)
        self.bot.repo_client.create_check_run.assert_called_once()

    def test_create_initial_check_run(self):
        """ Test that this properly uses the class attributes to create the
        initial check body. """
        commit_sha = '123qwer567'
        result = self.bot._create_initial_check_run(commit_sha)
        self.assertEqual(self.bot.initialize_title, result.get('output').get('title'))
        self.assertEqual(self.bot.initialize_summary, result.get('output').get('summary'))
        self.assertEqual(commit_sha, result.get('head_sha'))

    @patch.object(BasePRBot, '_should_reinitialize_check_run', Mock())
    def test_handle_reinitialize_event_invalid_event(self):
        """ Test that if an event other than the reinitialize event occurs then
        nothing will happen. """
        payload = {}
        self.bot._handle_reinitialize_event('bad-event', payload)
        self.bot._should_reinitialize_check_run.assert_not_called()

    def test_handle_reinitialize_event(self):
        """ Test that if an event occurs where the check run should be
        reinitialized then it is. If it shouldn't be initialized then it is
        not. """
        test_cases = [
            TestIteration(True, 1),
            TestIteration(False, 0),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if _should_reinitialize_check_run is {input} then _reinitialize_check_run is'
                              f' called {expected} times.'):
                self.setUp()
                with patch.multiple(BasePRBot, _should_reinitialize_check_run=Mock(return_value=input),
                                    _reinitialize_check_run=Mock()):
                    event = self.bot.reinitialize_event
                    payload = {}
                    self.bot._handle_reinitialize_event(event, payload)
                    self.assertEqual(self.bot._reinitialize_check_run.call_count, expected)

    def test_should_reinitialize_check_run(self):
        """ Test that the check run is only reinitialized if the status event
        is for the CI and its state is not success. """
        test_cases = [
            TestIteration({'state': 'pending', 'context': CI_STATUS_CONTEXT}, True),
            TestIteration({'state': 'success', 'context': CI_STATUS_CONTEXT}, False),
            TestIteration({'state': 'pending', 'context': 'wrong-context'}, False),
            TestIteration({'state': 'success', 'context': 'wrong-context'}, False),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if status payload is {input} then return {expected}.'):
                self.setUp()
                result = self.bot._should_reinitialize_check_run(input)
                self.assertEqual(result, expected)

    def test_get_commit_sha_from_reinitialize_event_payload(self):
        """ Test that the commit hash can be retrieved from the payload for
        reinitialization events. """
        test_cases = [
            TestIteration({'sha': 'hash'}, 'hash'),
            TestIteration({}, None),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if payload {input} the hash returned should be {expected}'):
                result = self.bot._get_commit_sha_from_reinitialize_event_payload(input)
                self.assertEqual(result, expected)

    def test_reinitialize_check_run(self):
        """ Test that the check run is created when _reinitialize_check_run is
        called and a check run exists. """
        check_details = {'name': self.bot.name, 'id': 123, 'status': 'completed'}
        self.bot.repo_client.get_commit_check_run_by_name.return_value = check_details

        payload = {'sha': 'hash'}
        self.bot._reinitialize_check_run(payload)
        self.bot.repo_client.create_check_run.assert_called_once()

    def test_reinitialize_check_run_missing_check_run(self):
        """ Test that if a check run does not exist it will be created
        instead of being updated. """
        check_details = None
        self.bot.repo_client.get_commit_check_run_by_name.return_value = check_details

        payload = {'sha': 'hash'}
        self.bot._reinitialize_check_run(payload)
        self.bot.repo_client.create_check_run.assert_called_once()

    @patch.object(BasePRBot, '_initialize_check_run', Mock())
    def test_reinitialize_check_run_do_nothing(self):
        """ Test that if the check run exists but is not in the completed
        status _reinitialize_check_run will perform no action """
        check_details = {'name': self.bot.name, 'id': 123}
        self.bot.repo_client.get_commit_check_run_by_name.return_value = check_details

        payload = {'sha': 'hash'}
        self.bot._reinitialize_check_run(payload)
        self.bot.repo_client.create_check_run.assert_not_called()

    @patch.object(BasePRBot, '_should_complete_check_run', Mock())
    def test_handle_completion_event_invalid_event(self):
        """ Test that if an event other than the completion even occurs then
        nothing will happen. """
        payload = {}
        self.bot._handle_completion_event('bad-event', payload)
        self.bot._should_complete_check_run.assert_not_called()

    def test_handle_completion_event(self):
        """ Test that if an event occurs where the check run should be
        completed then it is. If it shouldn't be completed then it is
        not. """
        test_cases = [
            TestIteration(True, 1),
            TestIteration(False, 0),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if _should_complete_check_run is {input} then _complete_check_run is called'
                              f' {expected} times.'):
                self.setUp()
                with patch.multiple(BasePRBot, _should_complete_check_run=Mock(return_value=input),
                                    _complete_check_run=Mock()):
                    event = self.bot.completion_event
                    payload = {}
                    self.bot._handle_completion_event(event, payload)
                    self.assertEqual(self.bot._complete_check_run.call_count, expected)

    @patch.object(BasePRBot, '_is_ci_complete', Mock())
    def test_should_complete_check_run(self):
        """ Test that if the event payload contains a commit hash then it will
        check to see if the ci is complete. """
        payload = {'sha': 'hash'}
        self.bot._should_complete_check_run(payload)
        self.bot._is_ci_complete.assert_called_once()

    def test_should_complete_check_run_missing_commit(self):
        """ Test that if there is no commit hash in the payload then the check
        should not be completed. """
        payload = {}
        result = self.bot._should_complete_check_run(payload)
        self.assertFalse(result)

    def test_get_commit_sha_from_completion_event_payload(self):
        """ Test that the commit hash can be retrieved from the payload for
        completion events. """
        test_cases = [
            TestIteration({'sha': 'hash'}, 'hash'),
            TestIteration({}, None),
        ]
        for input, expected in test_cases:
            with self.subTest(msg=f'if payload {input} the hash returned should be {expected}'):
                result = self.bot._get_commit_sha_from_completion_event_payload(input)
                self.assertEqual(result, expected)

    def test_is_ci_complete(self):
        """ Test that the it can determine if the ci is complete based on the
        commit status"""
        test_cases = [
            TestIteration({'state': 'success', 'context': CI_STATUS_CONTEXT}, True),
            TestIteration({'context': 'another app'}, False),
            TestIteration({}, False),
            TestIteration({'context': CI_STATUS_CONTEXT, 'state': 'failed'}, False),
        ]

        for input, expected in test_cases:
            with self.subTest(msg=f'on get_commit_status response of {input} _is_ci_complete should return'
                              f' {expected}'):
                self.setUp()
                result = self.bot._is_ci_complete(input)
                self.assertEqual(result, expected)

    def test_complete_check_run_missing_commit(self):
        """ Test that if the event payload is missing a commit hash the check
        run will not be completed. """
        payload = {}
        self.bot._complete_check_run(payload)
        self.bot.repo_client.get_commit_check_run_by_name.assert_not_called()

    def test_complete_check_run(self):
        """ Test that a check run is updated with a completed status if the
        check run has already been initialized. """
        check_run = {'name': self.bot.name, 'id': 123}
        self.bot.repo_client.get_commit_check_run_by_name.return_value = check_run
        complete_check_body = {}
        with patch.object(BasePRBot, '_create_complete_check_run', Mock(return_value=complete_check_body)):
            payload = {'sha': 'hash'}
            self.bot._complete_check_run(payload)
            self.bot.repo_client.update_check_run.assert_called_with(check_run.get('id'), complete_check_body)

    def test_complete_check_run_not_initialized(self):
        """ Test that a check run is created with a completed status if the
        check run has not been initialized """
        self.bot.repo_client.get_commit_check_run_by_name.return_value = None
        complete_check_body = {}
        with patch.object(BasePRBot, '_create_complete_check_run', Mock(return_value=complete_check_body)):
            payload = {'sha': 'hash'}
            self.bot._complete_check_run(payload)
            self.assertTrue('head_sha' in self.bot.repo_client.create_check_run.call_args.args[0])

    def test_complete_check_run_add_pr_comment(self):
        """ Test that completing a check will also add a PR comment if
        `should_add_pr_comment` is True. Otherwise no PR comment is added. """
        test_cases = [
            TestIteration(True, 1),
            TestIteration(False, 0)
        ]

        for input, expected in test_cases:
            with self.subTest(msg=f'when should_add_pr_comment is {input} then create_pr_comments_for_commit should'
                              f' execute {expected} times.'):
                self.setUp()
                self.bot.should_add_pr_comment = input
                self.bot.repo_client.get_commit_check_run_by_name.return_value = {'name': self.bot.name}
                complete_check_body = {}
                comment = 'comment'
                with patch.multiple(BasePRBot, _create_complete_check_run=Mock(return_value=complete_check_body),
                                    _create_check_complete_pr_comment=Mock(return_value=comment)):
                    payload = {'sha': 'hash'}
                    self.bot._complete_check_run(payload)
                    self.assertEqual(self.bot.repo_client.create_pr_comments_for_commit.call_count, expected)
                    if expected > 0:
                        commit_sha = payload.get('sha')
                        self.bot.repo_client.create_pr_comments_for_commit.assert_called_with(commit_sha, comment)

    def test_create_complete_check_run(self):
        """ Test that the complete check run request body is created correctly.
        """
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

        with patch.multiple(BasePRBot, _get_conclusion_data=Mock(return_value='data'),
                            _get_conclusion=Mock(return_value=conclusion),
                            _generate_conclusion_markdown=Mock(return_value=text)):
            payload = {}
            result = self.bot._create_complete_check_run(payload)
            self.assertEqual(result.get('name'), self.bot.name)
            self.assertEqual(result.get('status'), 'completed')
            self.assertEqual(result.get('conclusion'), conclusion)
            self.assertEqual(result.get('output').get('title'), title)
            self.assertEqual(result.get('output').get('summary'), summary)
            self.assertEqual(result.get('output').get('text'), text)

    def test_create_check_complete_pr_comment(self):
        """ Test that creating the comment gets the conclusion data and passes
        the data to `_generate_pr_comment_markdown`. """
        data = 'data'
        with patch.multiple(BasePRBot, _get_conclusion_data=Mock(return_value=data),
                            _generate_pr_comment_markdown=Mock()):
            payload = {}
            self.bot._create_check_complete_pr_comment(payload)
            self.bot._get_conclusion_data.assert_called_once()
            self.bot._generate_pr_comment_markdown.assert_called_once_with(data)
