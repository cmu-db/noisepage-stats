from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

service_start_time = datetime.now()

class HealthViewSet(viewsets.ViewSet):
    """
    Check whether the service is up and get how long it has been up
    """
    def list(self,request):
        uptime = (datetime.now() - service_start_time).total_seconds()
        data = {'uptime': '{} seconds'.format(uptime)}
        return Response(data, status=status.HTTP_200_OK)
