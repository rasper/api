from django.db import models

class BurnCool(models.Model):
    STATUS_CHOICES = (
        ('burn', 'Sit Down'),
        ('cool', 'Stand Up'),
    )
    status = models.CharField(choices=STATUS_CHOICES)
    created_at = models.DateTimeFIeld(auto_now_add=True)
