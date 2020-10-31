from rest_framework.viewsets import ViewSet 
from rest_framework.response import Response 
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from github3 import GitHub
import time
from jwt import JWT, jwk_from_pem
import requests

# Secrets that will eventuall have to move
GITHUB_PRIVATE_KEY= """"""
GITHUB_APP_IDENTIFIER = 86997
GITHUB_WEBHOOK_SECRET = 'incrudibles'
ALLOWED_EVENTS = ['pull_request', 'check_suite','check_run']

class NoisePageRepoClient():
    def __init__(self, private_key, app_id):
        self.git_client = GitHub()
        self.git_client.login_as_app(private_key_pem=str.encode(GITHUB_PRIVATE_KEY),app_id=GITHUB_APP_IDENTIFIER)
        self.owner = 'cmu-mse-cmudb'
        self.repo = 'terrier'
        self.noisepage_repo_client = self.git_client.app_installation_for_repository(self.owner,self.repo)

        #self.git_client.login_as_app_installation(private_key_pem=str.encode(GITHUB_PRIVATE_KEY),app_id=GITHUB_APP_IDENTIFIER,installation_id=self.noisepage_repo_client.id)

    def is_valid_installation_id(self, id):
        return id == self.noisepage_repo_client.id

    def _get_jwt(self):
        """
        This is needed to retrieve the installation access token (for debugging). 
        
        Useful for debugging purposes.  Must call .decode() on returned object to get string.
        """
        jwt = JWT()
        now = int(time.time())
        payload = {
            "iat": now,
            "exp": now + (60),
            "iss": GITHUB_APP_IDENTIFIER
        }
        private_key = jwk_from_pem(str.encode(GITHUB_PRIVATE_KEY,'utf-8'))
        return jwt.encode(payload, private_key, alg='RS256')

    def _get_installation_access_token(self):
        "Get the installation access token for debugging."
        headers = {'Authorization': f'Bearer {self._get_jwt()}',
                'Accept': 'application/vnd.github.machine-man-preview+json'}
        
        response = requests.post(url=self.noisepage_repo_client.access_tokens_url, headers=headers)
        response.raise_for_status()
        return response.json()['token']

    def create_check_run(self,sha):
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/check-runs"
        body = {
            "name":"performance-cop",
            "head_sha": f"{sha}"
        }
        response = requests.post(url=url,json=body,headers=headers)
        response.raise_for_status()

    def update_check_run(self, check_run_id):
        token = self._get_installation_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            "Accept": "application/vnd.github.v3+json"
        }
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/check-runs/{check_run_id}"
        body = {
            "name":"performance-cop",
            "status": "completed",
            "conclusion":"success",
            "output":{
                "title":"You are a performance hero!",
                "summary":"This PR actually improved the performance. Nice Job!",
                "text":"You improved performance of test x by 1%\n you improved b by 2% \n c by 3% yada yada yada"
            }
        }
        response = requests.patch(url=url,json=body,headers=headers)
        response.raise_for_status()
    

#TODO: add github3.py to requirements.txt
class GitEventsViewSet(ViewSet):

    def create(self,request):
        payload = JSONParser().parse(request)

        if not any([event in payload for event in ALLOWED_EVENTS]):
            return Response({"message":"This app is only designed to handle check_suite events"},status=HTTP_400_BAD_REQUEST)
        
        repo_client = NoisePageRepoClient(private_key=GITHUB_PRIVATE_KEY, app_id=GITHUB_APP_IDENTIFIER)
        if(not repo_client.is_valid_installation_id(payload.get('installation',{}).get('id'))):
            return Response({"message":"This app only works with the NoisePage repo"},status=HTTP_400_BAD_REQUEST)

        if 'check_suite' in payload:
            handle_check_suite_event(repo_client, payload)
        if 'pull_request' in payload:
            handle_pull_request_event(repo_client, payload)
        if 'check_run' in payload:
            handle_check_run_event(repo_client, payload)

        
        return Response(status=HTTP_200_OK)


def handle_check_suite_event(repo_client, payload):
    try:
        if payload.get('action')!= 'completed':
            repo_client.create_check_run(payload['check_suite'].get('head_sha'))
    except Exception as err:
        print(err)

def handle_check_run_event(repo_client, payload):
    # TODO: This is very temporary code to allow me to test this better
    if payload.get('action')!= 'completed':
        repo_client.update_check_run(payload['check_run'].get('id'))

def handle_pull_request_event(repo_client, payload):
    # TODO: probably want some logic for labels
    repo_client.create_check_run(payload['pull_request'].get('head',{}).get('sha'))