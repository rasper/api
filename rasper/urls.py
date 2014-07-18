from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from burncool.views import EventViewSet

router = routers.DefaultRouter()
router.register('event', EventViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rasper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^sit-duration/', 'burncool.views.duration', name='sit-duration'),
    url(r'^sit-report/', 'burncool.views.report', name='sit-report'),

    url(r'^$', 'rasper.views.api_root',
        name='api-root'),
) + router.urls
