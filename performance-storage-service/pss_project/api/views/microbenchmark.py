from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from pss_project.api.serializers.rest.MicrobenchmarkSerializer import MicrobenchmarkSerializer
from pss_project.api.serializers.database.MicrobenchmarkResultSerializer import MicrobenchmarkResultSerializer
from rest_framework.authentication import BasicAuthentication


class MicrobenchmarkViewSet(viewsets.ViewSet):
    """
    Store new microbenchmark results in the database
    """

    def create(self, request):
        user = BasicAuthentication().authenticate(request)
        if user is None:
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        data = JSONParser().parse(request)
        api_serializer = MicrobenchmarkSerializer(data=data)
        if not api_serializer.is_valid():
            return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        api_serializer.save()
        db_serializer = MicrobenchmarkResultSerializer(data=api_serializer.instance.convert_to_db_json())
        if not db_serializer.is_valid():
            return Response(db_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            db_serializer.save()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(api_serializer.validated_data, status=status.HTTP_201_CREATED)
