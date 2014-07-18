from datetime import datetime
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from burncool.models import BurnCool

class EventViewSet(viewsets.ModelViewSet):
    model = BurnCool

@api_view(['GET'])
def duration(request):
    last_event = BurnCool.objects.latest('start_at')
    time_diff= datetime.now() - last_event.start_at
    time_diff_in_minutes = time_diff.seconds // 60
    return Response(time_diff_in_minutes)

@api_view(['GET'])
def report(request):

    return Response({
        'hourly': hourly,
        'daily': daily,
        'monthly': monthly,
        'annually': annually,
    })
