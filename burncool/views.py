from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response

from burncool.models import BurnCool

class EventViewSet(viewsets.ModelViewSet):
    model = BurnCool

@api_view(['GET'])
def duration(request):

    return Response({
        'hourly': hourly,
        'daily': daily,
        'monthly': monthly,
        'annually': annually,
    })
