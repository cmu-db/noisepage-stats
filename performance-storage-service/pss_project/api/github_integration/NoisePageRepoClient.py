import time
import requests
from github3 import GitHub
from jwt import JWT, jwk_from_pem
import logging

from pss_project.api.constants import REPO_OWNER, REPO_NAME, GITHUB_BASE_URL

logger = logging.getLogger()


class NoisePageRepoClient():
    """ Class for communicating with GitHub.

    Attributes
    ----------
    private_key : str
        The private key of the GitHub App.
    owner : str
        The GitHub username of the repository owner.
    repo : str
        The name of the GitHub repo.
    git_client : GitHub object
        The client used to communicate with GitHub.
    noisepage_repo_client : Installation
        The client used to communicate with GitHub as the GitHub App
        installation.
    access_token : dict
        An access_token for authentication.
    """

    def __init__(self, private_key, app_id):
        """ Connect to github and create a Github client and a client specific
        to the Github app installation.

        Parameters
        ----------
        private_key : str
            The private key of the Github App.
        app_id : int
            The unique id of the Github App.
        """
        self.private_key = private_key
        self.owner = REPO_OWNER
        self.repo = REPO_NAME

        self.git_client = GitHub()
        self.git_client.login_as_app(private_key_pem=str.encode(private_key), app_id=app_id)
        self.noisepage_repo_client = self.git_client.app_installation_for_repository(self.owner, self.repo)
        self.access_token = {"token": None, "exp": 0}

    def is_valid_installation_id(self, id):
        """ Check whether an installation ID is the NoisePage installation.

        This will prevent other Github users from using the app.

        Parameters
        ----------
        id : int
            The id of the GitHub App installation.

        Returns
        -------
        bool
            True if the id matches an allowed GitHub App installation.
            False otherwise.
        """
        return id == self.noisepage_repo_client.id

    def _get_jwt(self):
        """ This creates a JWT that can be used to retrieve an authentication
        token for the GitHub app.

        Returns
        -------
        dict
            A dict containing the 'jwt' and expiration datetime.
        """
        jwt = JWT()
        now = int(time.time())
        payload = {
            "iat": now,
            "exp": now + (60),
            "iss": self.noisepage_repo_client.app_id
        }
        private_key = jwk_from_pem(str.encode(self.private_key))
        return {"jwt": jwt.encode(payload, private_key, alg='RS256'), "exp": payload.get('exp')}

    def _get_installation_access_token(self):
        """ Get the installation access token for making API calls not
        supported by github3.py.

        Only get a new token if the current one has expired. This sets the
        class's `access_token` attribute to the new token and updates the
        `exp`.

        Returns
        -------
        str
            The access token needed to make authenticated requests to GitHub.
        """
        if time.time() >= self.access_token.get('exp'):
            auth_token = self._get_jwt()
            headers = {'Authorization': f'Bearer {auth_token.get("jwt")}',
                       'Accept': 'application/vnd.github.v3+json'}
            response = requests.post(url=self.noisepage_repo_client.access_tokens_url, headers=headers)
            response.raise_for_status()
            self.access_token = {"token": response.json().get('token'), "exp": auth_token.get('exp')}
        return self.access_token.get('token')

    def create_check_run(self, create_body):
        """ Create a check run.

        Parameters
        ----------
        create_body : dict
            The body of the request that will create a new check run.

        Returns
        -------
        Response
            The response of the API request.

        Raises
        ------
        HTTPError
            If the API request failed.
        """
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"{GITHUB_BASE_URL}repos/{self.owner}/{self.repo}/check-runs"
        response = requests.post(url=url, json=create_body, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_check_run(self, check_run_id, update_body):
        """ Update a check run to mark it as complete.

        This is typically used to mark the check run as complete.

        Parameters
        ----------
        check_run_id : int
            The id of the check run to be updated.
        update_body : dict
            The body of the request that will create a new check run.

        Returns
        -------
        Response
            The response of the API request.

        Raises
        ------
        HTTPError
            If the API request failed.
        """
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"{GITHUB_BASE_URL}repos/{self.owner}/{self.repo}/check-runs/{check_run_id}"
        response = requests.patch(url=url, json=update_body, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_commit_status(self, commit_sha):
        """ Get the status of a commit.

        This was originally used to check if the CI was complete but this lead
        to timing issues because the API endpoint isn't strictly consistent.
        An event could be sent to say the CI is complete but this endpoint will
        say that it is still pending.

        Parameters
        ----------
        commit_sha : str
            The commit hash to check the status of.

        Returns
        -------
        Response
            The response of the API request.

        Raises
        ------
        HTTPError
            If the API request failed.
        """
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"{GITHUB_BASE_URL}repos/{self.owner}/{self.repo}/commits/{commit_sha}/status"
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_pr_comments_for_commit(self, commit_sha, comment_body):
        """ Add a comment to all PRs that a commit is associated with.

        Parameters
        ----------
        commit_sha : str
            The commit to add comments for.
        comment_body : str
            The comment to be added to the PRs. Markdown is accepted.
        """
        pr_numbers = self.find_commit_pr_numbers(commit_sha)
        for pr_number in pr_numbers:
            pull_request = self.noisepage_repo_client.pull_request(self.owner, self.repo, pr_number)
            pull_request.create_comment(comment_body)

    def find_commit_pr_numbers(self, commit_sha):
        """ Get the PR numbers for all open PRs associated with a commit.

        Parameters
        ----------
        commit_sha : str
            The commit to find the PRs for.

        Returns
        -------
        list of int
            The PR numbers that are associated with this commit.
        """
        search_query = f'{commit_sha}+type:pr+repo:{self.owner}/{self.repo}+state:open'
        prs = self.git_client.search_issues(search_query)
        logger.debug(f'search results: {prs}')
        return [pr.number for pr in prs]

    def get_commit_check_run_by_name(self, commit_sha, name):
        """ Get the check runs for a commit.

        This is typically used to find the check run, in order to discover its
        id.

        Parameters
        ----------
        commit_sha : str
            The commit for which the check run was created.
        name : str
            The name of the check.

        Returns
        -------
        check : dict
            The check run that was created for the commit that matches the name
            parameter. If no check matches the name, then this is an empty
            dict.

        Raises
        ------
        HTTPError
            If the API request failed.
        """
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"{GITHUB_BASE_URL}repos/{self.owner}/{self.repo}/commits/{commit_sha}/check-runs"
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        check_runs = response.json()
        check = find_check_run_by_name(check_runs.get('check_runs'), name)
        if check:
            return check
        return {}


def find_check_run_by_name(check_runs, name):
    """ Search through a list of check runs to see if it contains
    a specific check run based on the name.

    If the check run is not found this returns 'None'.

    Parameters
    ----------
    check_runs : list of dict
        An array of check runs. This can be an empty array.
    name : str
        The name of the check.

    Returns
    -------
    check : dict
        The check run that was created for the commit that matches the name
        parameter. If no check matches the name, then this is an empty
        dict.
    """
    for check in check_runs:
        if check.get('name') == name:
            return check
    return None
