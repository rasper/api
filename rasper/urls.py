from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from burncool.views import EventViewSet, ConfigurationViewSet

router = routers.DefaultRouter()
router.register('event', EventViewSet)
router.register('configuration', ConfigurationViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rasper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^sit-duration/', 'burncool.views.duration', name='sit-duration'),
    url(r'^sit-report/', 'burncool.views.report', name='sit-report'),
    url(r'^sit-daily-activity/', 'burncool.views.sit_daily_activity',
        name='sit-daily-activity'),

    url(r'^$', 'rasper.views.api_root',
        name='api-root'),
) + router.urls
