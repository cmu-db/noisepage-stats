import time
import requests
from github3 import GitHub
from jwt import JWT, jwk_from_pem
import logging

from pss_project.api.constants import REPO_OWNER, REPO_NAME, GITHUB_BASE_URL

logger = logging.getLogger()


class NoisePageRepoClient():
    def __init__(self, private_key, app_id):
        """ Connect to github and create a Github client and a client specific
        to the Github app installation"""
        self.private_key = private_key
        self.owner = REPO_OWNER
        self.repo = REPO_NAME

        self.git_client = GitHub()
        self.git_client.login_as_app(private_key_pem=str.encode(private_key), app_id=app_id)
        self.noisepage_repo_client = self.git_client.app_installation_for_repository(self.owner, self.repo)
        self.access_token = {"token": None, "exp": 0}

    def is_valid_installation_id(self, id):
        """ Check whether an installation ID is the NoisePage installation
        This will prevent other Github users from using the app """
        return id == self.noisepage_repo_client.id

    def _get_jwt(self):
        """ This creates a JWT that can be used to retrieve an authentication
        token for the Github app."""
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
        supported by github3.py. Only get a new token if the current one has
        expired. """
        if time.time() >= self.access_token.get('exp'):
            auth_token = self._get_jwt()
            headers = {'Authorization': f'Bearer {auth_token.get("jwt")}',
                       'Accept': 'application/vnd.github.v3+json'}
            response = requests.post(url=self.noisepage_repo_client.access_tokens_url, headers=headers)
            response.raise_for_status()
            self.access_token = {"token": response.json().get('token'), "exp": auth_token.get('exp')}
        return self.access_token.get('token')

    def create_check_run(self, create_body):
        """ Create a check run for the performance cop """
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
        """ Update a check run to mark it as complete """
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
        """ Get the status of a commit """
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"{GITHUB_BASE_URL}repos/{self.owner}/{self.repo}/commits/{commit_sha}/status"
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_commit_check_run_by_name(self, commit_sha, name):
        """ Get the check runs for a commit """
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
    for check in check_runs:
        if check.get('name') == name:
            return check
    return None
