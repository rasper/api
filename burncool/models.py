from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save


class BurnCool(models.Model):
    EVENT_CHOICES = (
        ('burn', 'Sit Down'),
        ('cool', 'Stand Up'),
    )
    event = models.CharField(max_length=4, choices=EVENT_CHOICES)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, editable=False)


def end_previous_event(sender, instance, **kwargs):
    try:
        last_event = BurnCool.objects.order_by('-start_at')[0]
    except IndexError:
        return

    BurnCool.objects.filter(pk=last_event.pk).update(end_at=datetime.now())


pre_save.connect(end_previous_event, BurnCool)
