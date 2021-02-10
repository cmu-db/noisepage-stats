import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from pss_project.api.constants import CI_STATUS_CONTEXT

logger = logging.getLogger()

# Github API keywords used to define the check's conclusion
CONCLUSION_SUCCESS = 'success'
CONCLUSION_NEUTRAL = 'neutral'
CONCLUSION_FAILURE = 'failure'

CONCLUSION_KEYS = [CONCLUSION_SUCCESS, CONCLUSION_NEUTRAL, CONCLUSION_FAILURE]


class BasePRBot():
    """ Abstract base class for GitHub PR Bot.

    Attributes
    ----------
    name : str
        The name you want to appear as the GitHub Check.
    repo_client : NoisePageRepoClient
        The GitHub client used to communicate via GitHub APIs.
    initialize_event : str
        The name of the event that will initialize the GitHub Check.
    initialize_actions : list of str
        The event actions that will initialize the GitHub Check. Some events do
        not have actions, in which case this should be `None`.
    initialize_title : str
        The title of the GitHub Check when it is initialized.
    initialize_summary : str
        The summary text of the GitHub Check when it is initialized.
    reinitialize_event : str
        The name of the event that will change a GitHub Check from a
        completed status to queued.
    reinitialize_actions : list of str
        The event actions that will reinitialize the GitHub Check. Some events
        do not have actions, in which case this should be `None`.
    completion_event : str
        The name of the event that will complete the GitHub Check.
    completion_actions : list of str
        The event actions that will complete the GitHub Check. Some events do
        not have actions, in which case this should be `None`.
    conclusion_title_map : dict
        A dict where the key is the conclusion keys and the value is the title
        for the given conclusion key.
    conclusion_summary_map : dict
        A dict where the key is the conclusion keys and the value is the
        summary for the given conclusion key.
    should_add_pr_comment : bool
        If True the PR bot will add a comment to the PR when the check is
        marked as complete.
    """

    __metaclass__ = ABCMeta

    def __init__(self, repo_client, name='generic-pr-bot'):
        """ Create a new GitHub PR Bot.

        Parameters
        ----------
        repo_client : NoisePageRepoClient
            The GitHub client used to communicate via GitHub APIs.
        name : str
            The name you want to appear as the GitHub Check.
        """
        self.name = name
        self.repo_client = repo_client

        # Properties that instances may need to override
        self.initialize_event = 'pull_request'
        # https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#pull_request
        self.initialize_actions = ['synchronize', 'opened', 'reopened']
        self.initialize_title = 'Pending CI'
        self.initialize_summary = 'This check will run after the CI completes successfully'
        self.reinitialize_event = 'status'
        self.reinitialize_actions = None
        self.completion_event = 'status'
        self.completion_actions = None

        @abstractproperty
        def conclusion_title_map(self):
            """ A dict where the key is the conclusion keys and the value is
            the title for the given conclusion key. """
            pass

        @abstractproperty
        def conclusion_summary_map(self):
            """ A dict where the key is the conclusion keys and the value is
            the summary for the given conclusion key. """
            pass

        @abstractproperty
        def should_add_pr_comment(self):
            """ If True the PR bot will add a comment to the PR when the check is
            marked as complete. """
            pass

    def run(self, event, payload):
        """ Process the event and payload.

        The Github bot will pass the event and the event payload to the
        initialize, reinitalize, and complete handlers to determine which
        actions to perform.

        Parameters
        ----------
        event : str
            The name of the GitHub event that was sent to the API endpoint.
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.
        """
        self._handle_initialize_event(event, payload)
        self._handle_reinitialize_event(event, payload)
        self._handle_completion_event(event, payload)
        return

    def _handle_initialize_event(self, event, payload):
        """ When the initialize event is detected create a new GitHub check
        run.

        If the event is not the `initialize_event` do nothing.

        Parameters
        ----------
        event : str
            The name of the GitHub event that was sent to the API endpoint.
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.
        """
        if event != self.initialize_event:
            return

        logger.debug(f'{self.name} handling initialization event.')
        if self._should_initialize_check_run(payload):
            logger.debug(f'{self.name} initializing check run')
            self._initialize_check_run(payload)

    def _get_commit_sha_from_initialize_event_payload(self, payload):
        """ Get the commit hash from the payload of the initalization event.

        By default this assumes the `initialize_event` is a pull-request. If
        using a different event override this method.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        str
            The commit hash associated with the GitHub event.
        """
        return payload.get(self.initialize_event, {}).get('head', {}).get('sha')

    def _should_initialize_check_run(self, payload):
        """ Determine if the event should initialize a check run.

        By default this is based on whether the action is one of the
        `initialize_actions`. For different behavior override this method.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        bool
            True if the check run should be initalized. False otherwise.
        """
        action = payload.get('action')
        return action in self.initialize_actions or self.initialize_actions is None

    def _initialize_check_run(self, payload):
        """ Create the initial check run.

        The check run starts in the queued state. If there is no commit hash
        in the payload then do nothing.

        Parameters
        ----------
        commit_sha : str
            The commit hash the check run should be created for.
        """
        commit_sha = self._get_commit_sha_from_initialize_event_payload(payload)
        if not commit_sha:
            return

        initial_check_body = self._create_initial_check_run(commit_sha)
        self.repo_client.create_check_run(initial_check_body)
        logger.debug(f'{self.name} initialized check run')

    def _create_initial_check_run(self, commit_sha):
        """ Generate the body of the request to create the GitHub check run.

        Parameters
        ----------
        commit_sha : str
            The commit hash the check run should be created for.

        Returns
        -------
        dict
            The body of the request to initialize the GitHub check run.
        """
        return {
            "name": self.name,
            "head_sha": f"{commit_sha}",
            "status": "queued",
            "output": {
                "title": self.initialize_title,
                "summary": self.initialize_summary
            }
        }

    def _handle_reinitialize_event(self, event, payload):
        """ When the reinitialize event is detected create a GitHub check run
        in the queued state.

        If the event is not the `reinitialize_event` do nothing.

        Parameters
        ----------
        event : str
            The name of the GitHub event that was sent to the API endpoint.
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.
        """
        if event != self.reinitialize_event:
            return

        logger.debug(f'{self.name} handling reinitialization event.')
        if self._should_reinitialize_check_run(payload):
            logger.debug(f'{self.name} reinitializing check run')
            self._reinitialize_check_run(payload)

    def _should_reinitialize_check_run(self, payload):
        """ Determine if the check run should be reinitialized.

        By default this method will check to see if the CI was started. This is
        key in the cases where developers re-run the CI. Override this method
        if a different condition is needed.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        bool
            True if the check run needs to be reinitialized. False otherwise.
        """
        state = payload.get('state')
        context = payload.get('context')
        logger.debug(f'status context: {context}, state: {state}')
        return context == CI_STATUS_CONTEXT and state != 'success'

    def _get_commit_sha_from_reinitialize_event_payload(self, payload):
        """ Get the commit hash from the payload of the reinitalization event.

        By default this assumes the `reinitialize_event` is a status. If
        using a different event override this method.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        str
            The commit hash associated with the GitHub event.
        """
        return payload.get('sha')

    def _reinitialize_check_run(self, payload):
        """ Update a check run back to the inital queued state.

        If a check run does not exist for the commit then create a new one.
        If there is no commit hash for the event then do nothing.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.
        """
        commit_sha = self._get_commit_sha_from_reinitialize_event_payload(payload)
        if not commit_sha:
            return

        initial_check_body = self._create_initial_check_run(commit_sha)
        check_run = self.repo_client.get_commit_check_run_by_name(commit_sha, self.name)
        if not check_run:
            self._initialize_check_run(commit_sha)
        elif check_run.get('status') == 'completed':
            self.repo_client.update_check_run(check_run.get('id'), initial_check_body)

    def _handle_completion_event(self, event, payload):
        """ When the completion event is detected mark the GitHub check run as
        complete.

        If the event is not the `completion_event` do nothing. Also add a
        comment to the PR when complete, if necessary.

        Parameters
        ----------
        event : str
            The name of the GitHub event that was sent to the API endpoint.
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.
        """
        if event != self.completion_event:
            return

        logger.debug(f'{self.name} handling completion event')
        if self._should_complete_check_run(payload):
            logger.debug(f'{self.name} completing check run')
            self._complete_check_run(payload)

    def _should_complete_check_run(self, payload):
        """ A check to determine if the check run should be updated as
        complete.

        By default this is based on whther the Jenkins CI status has
        been updated as success. Override this method for different behavior.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        bool
            True if the check run should be completed. False otherwise.
        """
        commit_sha = self._get_commit_sha_from_completion_event_payload(payload)
        if not commit_sha:
            return False

        return self._is_ci_complete(payload)

    def _get_commit_sha_from_completion_event_payload(self, payload):
        """ Get the commit hash from the payload of the completion event.

        By default this assumes the `completion_event` is the same as the
        `reinitialize_event. If using a different event override this method.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        str
            The commit hash associated with the GitHub event.
        """
        return self._get_commit_sha_from_reinitialize_event_payload(payload)

    def _is_ci_complete(self, payload):
        """ Check whether a status update indicates that the Jenkins pipeline
        is complete.

        CI completion is based on the state and the context of the status.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        bool
            True if the CI is complete. False otherwise.
        """
        state = payload.get('state')
        context = payload.get('context')
        logger.debug(f'status context: {context}, state: {state}')
        return context == CI_STATUS_CONTEXT and state == 'success'

    def _complete_check_run(self, payload):
        """ Update the check run with a completed state based on the performance
        results.

        If the check run does not exist create it in the completed state.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.
        """
        commit_sha = self._get_commit_sha_from_completion_event_payload(payload)
        if not commit_sha:
            return

        check_run = self.repo_client.get_commit_check_run_by_name(commit_sha, self.name)
        complete_check_body = self._create_complete_check_run(payload)
        if check_run:
            self.repo_client.update_check_run(check_run.get('id'), complete_check_body)
            logger.debug('Check run updated with check results')
        else:
            complete_check_body['head_sha'] = commit_sha
            self.repo_client.create_check_run(complete_check_body)
            logger.debug('Check run created in the completed state')

        if self.should_add_pr_comment:
            comment_body = self._create_check_complete_pr_comment(payload)
            self.repo_client.create_pr_comments_for_commit(commit_sha, comment_body)
            logger.debug('PRs updated with comment')

    def _create_complete_check_run(self, payload):
        """ Create a check run request body to make a check run as complete.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        dict
            The body of the request to update the GitHub check run as complete.
        """
        data = self._get_conclusion_data(payload)
        conclusion = self._get_conclusion(data)
        return {
            "name": self.name,
            "status": "completed",
            "conclusion": conclusion,
            "output": {
                "title": self.conclusion_title_map.get(conclusion),
                "summary": self.conclusion_summary_map.get(conclusion),
                "text": self._generate_conclusion_markdown(data),
            },
        }

    def _create_check_complete_pr_comment(self, payload):
        """ Create a comment string for the PR.

        The comment is to give a summary of the check result. This is
        especially helpful if the CI is run multiple times. It keeps a history
        of the different results.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        str
            A string that will be displayed as a comment in the PR. Markdown is
            accepted.
        """
        data = self._get_conclusion_data(payload)
        return self._generate_pr_comment_markdown(data)

    @abstractmethod
    def _get_conclusion_data(self, payload):
        """ A method that returns all the data needed to determine the result
        of the check run.

        Parameters
        ----------
        payload : dict
            The payload of the GitHub event request that was sent to the API
            endpoint.

        Returns
        -------
        data
            The data needed to determine the check run conclusion.
        """
        pass

    @abstractmethod
    def _get_conclusion(self, data):
        """ A method that returns all the data needed to determine the result
        of the check run.

        Parameters
        ----------
        data :
            The data needed to determine the check run conclusion.

        Returns
        -------
        conclusion : str
            A string representing the result of the check run.
        """
        pass

    @abstractmethod
    def _generate_conclusion_markdown(self, data):
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

    @abstractmethod
    def _generate_pr_comment_markdown(self, data):
        """Generate the markdown content that will be added as a comment to the
        PR.

        If no comment should be added then this can return None.

        Parameters
        ----------
        data :
            The data needed to determine create the markdown comment.

        Returns
        -------
        markdown : str
            A string that will be displayed as a comment in the PR. Markdown is
            accepted.
        """
        pass
