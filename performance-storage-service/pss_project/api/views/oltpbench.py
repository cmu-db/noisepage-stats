from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from pss_project.api.serializers.rest.OLTPBenchSerializer import OLTPBenchSerializer
from datetime import datetime

service_start_time = datetime.now()

class OLTPBenchViewSet(viewsets.ViewSet):
    """
    Store a new OLTPBench result in the datatbase
    """
    def create(self,request):
        data = JSONParser().parse(request)
        serializer = OLTPBenchSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        #oltp_bench_result = serializer.save()
        # TODO: Transform the object into a database object
        return Response(serializer.data, status=status.HTTP_201_CREATED)



