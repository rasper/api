from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from burncool.models import BurnCool

class EventViewSet(viewsets.ModelViewSet):
    model = BurnCool

@api_view(['GET'])
def duration(request):
    last_event = BurnCool.objects.latest('start_at')
    if last_event.event == 'burn':
        time_diff = datetime.now() - last_event.start_at
        duration = time_diff.seconds
    else:
        duration = 0
    return Response(duration)



@api_view(['GET'])
def report(request):

    events = BurnCool.objects.filter(event='burn')

    hourly = events.aggregate_duration(timedelta(hours=1))
    daily = events.aggregate_duration(timedelta(days=1))
    monthly = events.aggregate_duration(timedelta(days=30))
    annually = events.aggregate_duration(timedelta(days=365))

    return Response({
        'hourly': hourly,
        'daily': daily,
        'monthly': monthly,
        'annually': annually,
    })

@api_view(['GET'])
def sit_activity(request, date):
    pass

