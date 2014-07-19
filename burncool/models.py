from datetime import datetime
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save

class BurnCoolQuerySet(models.query.QuerySet):
    def aggregate_duration(self, deltas):
        cutoff = datetime.now() - deltas
        duration = 0
        qs = self.filter(
                Q(start_at__gte=cutoff)
            ).exclude(
                end_at__isnull=True
            ).values('start_at', 'end_at')

        for event in qs:
            duration += (event['end_at'] - event['start_at']).seconds // 60


        try:
            event = self.filter(
                    Q(start_at__lte=cutoff, end_at__gte=cutoff)
                ).exclude(
                    end_at__isnull=True
                ).values('start_at', 'end_at')[0]
        except IndexError:
            pass
        else:
            duration += (event['end_at'] - event['start_at']).seconds // 60

        try:
            event = self.filter(
                    Q(end_at__isnull=True)
                ).values('start_at', 'end_at')[0]
        except IndexError:
            pass
        else:
            x = (datetime.now() - event['start_at']).seconds
            if x >= deltas.seconds:
                duration += deltas.seconds // 60
            else:
                duration += x // 60
        return duration


    def filter_by_date(self, dt):
        return self.filter(
            Q(end_at__year=dt.year, end_at__month=dt.month, end_at__day=dt.day),
            Q(start_at__year=dt.year, start_at__month=dt.month, start_at__day=dt.day),
        )

class BurnCoolManager(models.Manager):
    def get_queryset(self):
        return BurnCoolQuerySet(self.model)
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_queryset(), attr, *args)

class BurnCool(models.Model):
    EVENT_CHOICES = (
        ('burn', 'Sit Down'),
        ('cool', 'Stand Up'),
    )
    event = models.CharField(max_length=4, choices=EVENT_CHOICES)
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, editable=False)

    objects = BurnCoolManager()

    def duration(self):
        return self.end_at - self.start_at


def end_previous_event(sender, instance, **kwargs):
    try:
        last_event = BurnCool.objects.order_by('-start_at')[0]
    except IndexError:
        return

    BurnCool.objects.filter(pk=last_event.pk).update(end_at=datetime.now())


pre_save.connect(end_previous_event, BurnCool)
