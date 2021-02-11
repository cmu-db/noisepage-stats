import hmac
import logging

from rest_framework.viewsets import ViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from pss_project.api.github_integration.NoisePageRepoClient import NoisePageRepoClient
from pss_project.api.github_integration.PerformanceGuardBot import PerformanceGuardBot
from pss_project.api.constants import (GITHUB_WEBHOOK_HASH_HEADER, GITHUB_EVENT_HEADER, ALLOWED_EVENTS,
                                       GITHUB_APP_WEBHOOK_SECRET, GITHUB_APP_PRIVATE_KEY, GITHUB_APP_ID)

logger = logging.getLogger()


class GitEventsViewSet(ViewSet):

    def create(self, request):
        """ This endpoint is where all Github events are posted.

        This is where all the Github bots live. They are created and then the
        request is passed to each bot in sequence. The bot will perform any
        action that it needs to, based on the request. Afterwards the request
        will be passed to the next bot. If the request does not pertain to a
        bot it will do nothing.

        Parameters
        ----------
        request : Request
            The Github event POST request.

        Returns : Response
            The response to send back to Github based on the result of
            processing the request.
        """
        if not is_valid_github_webhook_hash(request.META.get(GITHUB_WEBHOOK_HASH_HEADER), request.body):
            # Check that the request actually came from Github by making sure the encrypted webhook secret
            # matches the secret we created.
            logger.debug('Invalid webhook hash')
            return Response({"message": "Invalid request hash. Only Github may call this endpoint."},
                            status=HTTP_403_FORBIDDEN)
        logger.debug('Valid webhook hash')

        payload = JSONParser().parse(request)
        event = request.META.get(GITHUB_EVENT_HEADER)

        if event not in ALLOWED_EVENTS:
            # Check that the event is one that we are expecting
            logger.debug(f'Received a non-allowed event: {event}')
            return Response({"message": f"This app is only designed to handle {ALLOWED_EVENTS} events"},
                            status=HTTP_400_BAD_REQUEST)
            
        repo_installation_id = payload.get('installation', {}).get('id')
        try:
            repo_client = NoisePageRepoClient(private_key=GITHUB_APP_PRIVATE_KEY, app_id=GITHUB_APP_ID)
            logger.debug('Authenticated with Github repo')
        except Exception as err:
            logger.debug(f'Received event for repo: {repo_installation_id}')
            return Response({'message': 'Failed to authenticate app with repository.'
                            ' This app only works with the NoisePage repo'},
                            status=HTTP_400_BAD_REQUEST)

        try:
            performance_guard = PerformanceGuardBot(repo_client=repo_client, name='performance-guard')
            performance_guard.run(event, payload)

        except Exception as err:
            logger.error(f'GitEventsViewSet create failed: {err}')
            return Response({"message": err.message if hasattr(err, 'message') else str(err)},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=HTTP_200_OK)


def is_valid_github_webhook_hash(hash_header, req_body):
    """ Check that the hash passed with the request is valid based on the
    webhook secret.

    Parameters
    ----------
    hash_header : str
        The Github hash header sent with the event.
    req_body : dict
        The body of the event sent by Github via a POST request.

    Returns
    -------
    bool
        If the hash is valid then this is True. False otherwise.
    """
    alg, req_hash = hash_header.split('=', 1)
    valid_hash = hmac.new(str.encode(GITHUB_APP_WEBHOOK_SECRET.strip()), req_body, alg)
    return hmac.compare_digest(req_hash, valid_hash.hexdigest())
