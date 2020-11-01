from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from pss_project.github_integration.NoisePageRepoClient import NoisePageRepoClient

# Secrets that will eventuall have to move
GITHUB_PRIVATE_KEY = """"""
GITHUB_APP_IDENTIFIER = 86997
ALLOWED_EVENTS = ['pull_request', 'state']
CI_STATUS_CONTEXT = 'continuous-integration/jenkins/pr-merge'


# TODO: add github3.py to requirements.txt
class GitEventsViewSet(ViewSet):

    def create(self, request):
        payload = JSONParser().parse(request)
        if not any([event in payload for event in ALLOWED_EVENTS]):
            return Response({"message": "This app is only designed to handle pull_request and status events"},
                            status=HTTP_400_BAD_REQUEST)

        repo_client = NoisePageRepoClient(private_key=GITHUB_PRIVATE_KEY, app_id=GITHUB_APP_IDENTIFIER)
        if(not repo_client.is_valid_installation_id(payload.get('installation', {}).get('id'))):
            return Response({"message": "This app only works with the NoisePage repo"}, status=HTTP_400_BAD_REQUEST)
        
        if 'pull_request' in payload:
            handle_pull_request_event(repo_client, payload)
        if 'state' in payload:
            handle_status_event(repo_client, payload)

        return Response(status=HTTP_200_OK)



def handle_status_event(repo_client, payload):
    commit_sha = payload.get('commit',{}).get('sha')
    status_response = repo_client.get_commit_status(commit_sha)
    if is_status_ci_complete(status_response):
        check_run = repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_IDENTIFIER)
        repo_client.update_check_run(check_run.get('id'), performance_check_result())

def performance_check_result():
    # TODO: This function will parse the results of the performance
    # comparison
    return {
        "name": "performance-cop",
        "status": "completed",
        "conclusion": "success",
        "output": {
            "title": "You are a performance hero!",
            "summary": "This PR actually improved the performance. Nice Job!",
            "text": "You improved performance of test x by 1%\n you improved b by 2% \n c by 3% yada yada yada"
        }
    }


def is_status_ci_complete(status_reponse):
    if status_reponse.get('state') != 'success': return False 
    return any([status.get('context') == CI_STATUS_CONTEXT for status in status_reponse.get('statuses',[])])

def handle_pull_request_event(repo_client, payload):
    # TODO: probably want some logic for labels
    repo_client.create_check_run(payload['pull_request'].get('head', {}).get('sha'))
