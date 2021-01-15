import logging

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from pss_project.api.github_integration.PerformanceGuardBot import PerformanceGuardBot
from pss_project.settings.utils import get_environ_value

logger = logging.getLogger()


class GitEventsViewSet(ViewSet):

    def create(self, request):
        """ This endpoint is where all Github events are posted. This is where
        all the Github bots live. They are created and then the request is
        passed to each bot in sequence. The bot will perform any action that
        it needs to, based on the request. Afterwards the request will be
        passed to the next bot. If the request does not pertain to a bot it
        will do nothing. """
        try:
            performance_guard = PerformanceGuardBot(app_id=86997,
                                                    private_key=get_environ_value('PERFORMANCE_GUARD_PRIVATE_KEY'),
                                                    webhook_secret=get_environ_value(
                                                        'PERFORMANCE_GUARD_WEBHOOK_SECRET'),
                                                    name='performance-guard')
            performance_guard.connect_to_repo()
            performance_guard.run(request)

        except Exception as err:
            logger.error(f'GitEventsViewSet create failed: {err}')
            return Response({"message": err.message if hasattr(err, 'message') else err},
                            status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=HTTP_200_OK)
