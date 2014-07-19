from datetime import datetime, timedelta
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from burncool.models import BurnCool, Configuration

class EventViewSet(viewsets.ModelViewSet):
    model = BurnCool

class ConfigurationViewSet(viewsets.ModelViewSet):
    model = Configuration
    queryset = Configuration.objects.order_by('-id')[:1]

@api_view(['GET'])
def duration(request):
    duration = 0
    try:
        last_event = BurnCool.objects.latest('start_at')
    except:
        pass
    else:
        if last_event.event == 'burn':
            time_diff = datetime.now() - last_event.start_at
            duration = time_diff.seconds
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
def sit_daily_activity(request):
    date = request.GET['date']
    cutoff = datetime.strptime(date, '%Y-%m-%d').date()
    burn_cools = BurnCool.objects.filter_by_date(cutoff)
    duration = 0
    interval = []
    for hr in range(0, 24):
        duration = 0
        for bc in burn_cools:
            if bc.end_at.hour == hr:
                if bc.start_at.hour == hr:
                    duration += bc.end_at.minute - bc.start_at.minute
                else:
                    duration += bc.end_at.minute
            elif bc.start_at.hour == hr:
                duration += 60 - bc.start_at.minute
        else:
            interval.append(duration)
    return Response(
        interval
    )


@api_view(['GET'])
def sit_weekly_activity(request):
    date = request.GET['date']
    cutoff = datetime.strptime(date, '%Y-%m-%d').date()
    burn_cools = BurnCool.objects.filter_by_date(cutoff)
    duration = 0
    interval = []
    for wd in range(0, 7):
        duration = 0
        for bc in burn_cools:
            if bc.end_at.weekday() == wd:
                if bc.start_at.weekday() == wd:
                    duration += bc.end_at.minute - bc.start_at.minute
                else:
                    duration += bc.end_at.minute
            elif bc.start_at.weekday() == wd:
                duration += 60 - bc.start_at.minute
        else:
            interval.append(duration)
    return Response(
        interval
    )



