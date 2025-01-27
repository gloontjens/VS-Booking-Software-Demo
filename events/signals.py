from .models import Global
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def check_gcal(sender, instance, **kwargs):
    #instance.profile.save()
    this = Global.objects.get(pk=1)
    this.gcal_needs = True
    this.save()
    instance.events.save()