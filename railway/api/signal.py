from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *
from user.models import User
from rails.models import *


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

@receiver(post_save, sender=Carriage)
def create_places(sender, instance, created, **kwargs):
    if created:
        for i in range(36):
            Places.objects.create(
                carriage=instance,
                number=i+1,
                status=True
            )