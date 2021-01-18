import logging

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from pss_project.api.serializers.rest.MicrobenchmarkSerializer import MicrobenchmarkSerializer
from pss_project.api.serializers.database.MicrobenchmarkResultSerializer import MicrobenchmarkResultSerializer
from rest_framework.authentication import BasicAuthentication

logger = logging.getLogger()


class MicrobenchmarkViewSet(viewsets.ViewSet):

    def create(self, request):
        """ First check that the an authorized user posted the request. Then validate the API request body. Next convert
        the request body into a format suitable for the database. Finally, store the new microbenchmark result in the
        database. """
        user = BasicAuthentication().authenticate(request)
        if user is None:
            logger.debug('Invalid authentication')
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        data = JSONParser().parse(request)
        api_serializer = MicrobenchmarkSerializer(data=data)
        if not api_serializer.is_valid():
            logger.debug(f'Bad Request: {api_serializer.errors}')
            return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        api_serializer.save()
        db_serializer = MicrobenchmarkResultSerializer(data=api_serializer.instance.convert_to_db_json())
        db_serializer.smudge_timestamp()
        if not db_serializer.is_valid():
            logger.error(f'Invalid db_serializer: {db_serializer.errors}')
            return Response(db_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            db_serializer.save()
        except Exception as err:
            logger.error(f'MicrobenchmarkViewSet create failed: {err}')
            return Response({'message': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(api_serializer.validated_data, status=status.HTTP_201_CREATED)
