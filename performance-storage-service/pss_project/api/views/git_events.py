import hmac
import logging

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from pss_project.api.github_integration.NoisePageRepoClient import NoisePageRepoClient
from pss_project.api.constants import (GITHUB_APP_IDENTIFIER, ALLOWED_EVENTS, CI_STATUS_CONTEXT, 
                                                    WEBHOOK_SECRET, GITHUB_WEBHOOK_HASH_HEADER, GITHUB_PRIVATE_KEY,
                                                    PERFORMANCE_COP_CHECK_NAME)

logger = logging.getLogger(__name__)

class GitEventsViewSet(ViewSet):

    def create(self, request):
        """ This is the endpoint that Github events are posted to """
        logger.critical("ARE We Logging")
        logger.info("Maybe")
        if not is_valid_github_webhook_hash(request.META.get(GITHUB_WEBHOOK_HASH_HEADER), request.body):
            return Response({"message":"Invalid request hash. Only Github may call this endpoint."},status=HTTP_403_FORBIDDEN)
        logger.debug('Valid webhook hash')

        payload = JSONParser().parse(request)
        event = request.META.get('HTTP_X_GITHUB_EVENT')
        
        logger.debug(f'Incoming {event} event')
        if not any([valid_event == event for valid_event in ALLOWED_EVENTS]):
            return Response({"message": f"This app is only designed to handle {ALLOWED_EVENTS} events"},
                            status=HTTP_400_BAD_REQUEST)

        try:
            repo_client = NoisePageRepoClient(private_key=GITHUB_PRIVATE_KEY, app_id=GITHUB_APP_IDENTIFIER)
            logger.debug('Authenticated with Github repo')

            if(not repo_client.is_valid_installation_id(payload.get('installation', {}).get('id'))):
                return Response({"message": "This app only works with the NoisePage repo"}, status=HTTP_400_BAD_REQUEST)

            if event == 'pull_request':
                handle_pull_request_event(repo_client, payload)
            if event == 'status':
                handle_status_event(repo_client, payload)
                
        except Exception as err:
            return Response({"message": err.message if hasattr(err,'message') else err}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(status=HTTP_200_OK)

def is_valid_github_webhook_hash(hash_header, req_body):
    """ Check that the has passed with the request is valid based on the
    webhook secret and the request body """
    alg, req_hash = hash_header.split('=',1)
    valid_hash = hmac.new(str.encode(WEBHOOK_SECRET),req_body, alg)
    return hmac.compare_digest(req_hash, valid_hash.hexdigest())

def handle_pull_request_event(repo_client, payload):
    """ When a pull request event is detected create a new check run for the 
    performance cop"""
    # TODO: Not sure if we want some logic for labels
    #TODO: This if statement is temporary so we can test in the NoisePage repo without affecting everyone
    if payload['pull_request'].get('user',{}).get('login') == 'bialesdaniel': 
        commit_sha = payload['pull_request'].get('head', {}).get('sha')
        if should_initialize_check_run(payload.get('action')):
            logger.debug('pull request reinitialized check')
            initialize_check_run(repo_client, commit_sha)
        if payload.get('action') == 'closed':
            logger.debug('pull request was closed')
            branch = payload['pull_request'].get('head',{}).get('ref')
            cleanup_check_run(branch)

def should_initialize_check_run(pull_request_action):
    """ Determine if the pull request event should initialize a check run """
    return any(pull_request_action == action for action in ['synchronize','opened','reopened'])

def initialize_check_run(repo_client, sha):
    """ Create the initial performance cop check run. The run starts in the
    queued state """
    create_body = create_initial_check_run(sha)
    repo_client.create_check_run(create_body)
    logger.debug('Initialized check run')

def create_initial_check_run(sha):
    return {
        "name": PERFORMANCE_COP_CHECK_NAME,
        "head_sha": f"{sha}",
        "status": "queued",
        "output": {
            "title": "Pending CI",
            "summary": "This check will run after CI completes successfully"
        }
    }

def cleanup_check_run(branch):
    #TODO: here we will delete performance results for the PR branch from the DB
    # I also need to check what Jenkins stores in the git_branch column cause it
    # might not be the same as the branch in the event. 
    logger.debug('Cleaning up check run')


def handle_status_event(repo_client, payload):
    """ When a status update event occurs check to see if it indicates that the
    ci/cd pipeline completed. If that is the case then results will be in the 
    database. Compare the performance results with the results from master and
    update the check run based on the results of the comparison """
    commit_sha = payload.get('commit',{}).get('sha')
    status_response = repo_client.get_commit_status(commit_sha)
    if is_ci_complete(repo_client, status_response):
        logger.debug('Status update indicated CI completed')
        complete_check_run(commit_sha)
    elif status_response.get('context') == CI_STATUS_CONTEXT:
        logger.debug('Status update indicated CI started')
        initialize_check_run_if_missing(repo_client, commit_sha)

def is_ci_complete(status_reponse):
    """ Check whether a status update indicates that the Jenkins pipeline
    is complete. This is based on the state and the context of the status """
    if status_reponse.get('state') != 'success': return False 
    return any([status.get('context') == CI_STATUS_CONTEXT for status in status_reponse.get('statuses',[])])

def complete_check_run(repo_client, commit_sha):
    """ Update the check run with a complete status based on the performance
    results. If the check run does not exist do nothing """
    check_run = repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_IDENTIFIER)
    if check_run: 
        repo_client.update_check_run(check_run.get('id'), performance_check_result())
        logger.debug('Check run updated with performance results')

def initialize_check_run_if_missing(repo_client, commit_sha):
    """ Check to see if the check run was already created. If it was not then
    initialize the check run """
    check_run = repo_client.get_commit_check_run_for_app(commit_sha, GITHUB_APP_IDENTIFIER)
    if not check_run:
        initialize_check_run(commit_sha)
        logger.debug('Check run did not exist. It has been initialized')

def performance_check_result():
    # TODO: This function will parse the results of the performance
    # comparison
    return {
        "name": PERFORMANCE_COP_CHECK_NAME,
        "status": "completed",
        "conclusion": "success",
        "output": {
            "title": "Feature coming soon",
            "summary": "This will tell you the impact your PR has on performance",
            "text": "This feature should be coming soon but we need to first make sure that the \
                Github integrations work"
        }
    }

