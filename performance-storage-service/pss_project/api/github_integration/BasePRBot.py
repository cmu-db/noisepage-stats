import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from pss_project.api.constants import CI_STATUS_CONTEXT, GITHUB_APP_ID

logger = logging.getLogger()

CONCLUSION_SUCCESS = 'success'
CONCLUSION_NEUTRAL = 'neutral'
CONCLUSION_FAILURE = 'failure'

CONCLUSION_KEYS = [CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL, CONCLUSION_FAILURE]


class BasePRBot():

    __metaclass__ = ABCMeta

    def __init__(self, repo_client, name='generic-pr-bot'):
        self.name = name
        self.repo_client = repo_client

        # Properties that instances may need to override
        self.allowed_events = ['pull_request', 'status']
        self.initialize_event = 'pull_request'
        self.initialize_actions = ['synchronize', 'opened', 'reopened']
        self.initialize_title = 'Pending CI'
        self.initialize_summary = 'This check will run after the CI completes successfully'
        self.completion_event = 'status'
        self.completion_actions = None

        # Properties that definitely should be overwritten
        @abstractproperty
        def conclusion_title_map(self):
            pass

        @abstractproperty
        def conclusion_summary_map(self):
            pass

    def run(self, event, payload):
        """First we make sure that the hash in the header is valid. This
        certifies that only someone who knows the WEBHOOK_SECRET can call this
        endpoint. Then we check to make sure the event is one of the events
        that we are expeting. Next we connect to the NoisePage repository and
        validate that the Github event is for the NoisePage repository.
        Currently we only support events from
        https://github.com/cmu-db/noisepage. Then the Github bot will pass the
        message body to the initialize and complete methods to determine which
        actions to perform."""

        self.handle_initialize_event(event, payload)
        self.handle_completion_event(event, payload)
        return

    def handle_initialize_event(self, event, payload):
        """ When the initialize event is detected create a new check run for
        the Github bot"""
        if event != self.initialize_event:
            return

        logger.debug(f'{self.name} handling initialization event')
        commit_sha = payload[self.initialize_event].get('head', {}).get('sha')
        if self.should_initialize_check_run(payload.get('action')):
            logger.debug(f'{self.name} initializing check run')
            self.initialize_check_run(commit_sha)

    def should_initialize_check_run(self, action):
        """ Determine if the event should initialize a check run """
        return action in self.initialize_actions or self.initialize_actions is None

    def initialize_check_run(self, commit_sha):
        """ Create the initial check run. The run starts in the queued state """
        initial_check_body = self.create_initial_check_run(commit_sha)
        self.repo_client.create_check_run(initial_check_body)
        logger.debug(f'{self.name} initialized check run')

    def create_initial_check_run(self, commit_sha):
        """ Generate the body of the request to create the github check run. """
        return {
            "name": self.name,
            "head_sha": f"{commit_sha}",
            "status": "queued",
            "output": {
                "title": self.initialize_title,
                "summary": self.initialize_summary
            }
        }

    def handle_completion_event(self, event, payload):
        """ When a completion event occurs check whether the check run should
        be completed. If it should then complete it."""
        if event != self.completion_event:
            return

        logger.debug(f'{self.name} handling completion event')
        if self.should_complete_check_run(payload):
            logger.debug(f'{self.name} completing check run')
            self.complete_check_run(payload)
        elif self.should_reinitialize_check_run(payload):
            self.initialize_check_run_if_missing(payload)

    def should_complete_check_run(self, payload):
        """ A check to determine if the check run should be updated as
        complete. By default this is based on whther the Jenkins CI status has
        been updated as success. Override this method for different behavior."""
        commit_sha = payload.get('commit', {}).get('sha')
        if not commit_sha:
            return False

        return self.is_ci_complete(commit_sha)

    def is_ci_complete(self, commit_sha):
        """ Check whether a status update indicates that the Jenkins pipeline
        is complete. This is based on the state and the context of the status """
        status_response = self.repo_client.get_commit_status(commit_sha)
        logger.debug(f'status response: {status_response.get("statuses",[])}')
        return (any([status.get('context') == CI_STATUS_CONTEXT and status.get('state') == 'success'
                     for status in status_response.get('statuses', [])]))

    def complete_check_run(self, payload):
        """ Update the check run with a complete status based on the performance
        results. If the check run does not exist do nothing """
        commit_sha = payload.get('commit', {}).get('sha')
        if not commit_sha:
            return

        check_run = self.repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_ID)
        if check_run:
            complete_check_body = self.create_complete_check_run(payload)
            self.repo_client.update_check_run(check_run.get('id'), complete_check_body)
            logger.debug('Check run updated with performance results')

    def create_complete_check_run(self, payload):
        """ Create a check run request body to make a check run as complete. Generate the status and output contents based
        on the comparison between this PRs performance results and the nightly build's performance results."""
        data = self.get_conclusion_data(payload)
        conclusion = self.get_conclusion(data)
        return {
            "name": self.name,
            "status": "completed",
            "conclusion": conclusion,
            "output": {
                "title": self.conclusion_title_map.get(conclusion),
                "summary": self.conclusion_summary_map.get(conclusion),
                "text": self.generate_conclusion_markdown(data),
            },
        }

    @abstractmethod
    def get_conclusion_data(self, payload):
        """ A method that returns all the data needed to determine the result
        of the check.

        Parameters
        ----------
        payload : dict
            The payload of the request sent from Github

        Returns
        -------
        data
            The data needed to determine the check conclusion
        """
        pass

    @abstractmethod
    def get_conclusion(self, data):
        """ A method that returns all the data needed to determine the result
        of the check.

        Parameters
        ----------
        data :
            The data needed to determine the check conclusion

        Returns
        -------
        conclusion : str
            A string representing the result of the check
        """
        pass

    @abstractmethod
    def generate_conclusion_markdown(self, data):
        """Generate the markdown content that will show up in the detailed view
        of the check run.

        Parameters
        ----------
        data :
            The data needed to determine the check conclusion

        Returns
        -------
        markdown : str
            A string that will be displayed in the check details. Markdown is
            accepted.
        """
        pass

    def should_reinitialize_check_run(self, payload):
        """ Determine if the check run should be reinitialized. By default this
        method will check to see if the CI was started. This is key in the
        cases where developers re-run the CI. Override this method if a
        a different condition is needed."""
        if 'status' not in payload:
            return False

        commit_sha = payload.get('commit', {}).get('sha')
        status_response = self.repo_client.get_commit_status(commit_sha)
        return (any([status.get('context') == CI_STATUS_CONTEXT for status in status_response.get('statuses', [])]) and
                status_response.get('state') != 'success')

    def initialize_check_run_if_missing(self, payload):
        """ Check to see if the check run was already created. If it was not then
        initialize the check run """
        commit_sha = payload.get('commit', {}).get('sha')
        check_runs = self.repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_ID)
        if not check_runs or not any([check_run.get('name') == self.name for check_run in check_runs.get('check_runs', [])]):
            logger.debug(f'{self.name} check run does not exist -- initializing.')
            self.initialize_check_run(commit_sha)
