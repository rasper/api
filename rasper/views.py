from rest_framework import renderers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny


@api_view(('GET',))
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'events': reverse('burncool-list', request=request,
            format=format),
        'sit-duration': reverse('sit-duration', request=request,
            format=format),
        'sit-reports': reverse('sit-report', request=request,
            format=format),
        'sit-daily-activity': reverse('sit-daily-activity', request=request,
            format=format),
        'configuration': reverse('configuration-list', request=request,
            format=format),
        })

