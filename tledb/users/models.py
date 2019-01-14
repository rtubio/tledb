
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from fetcher.models import tle


class Profile(models.Model):
    """
    This class holds additional data required from each user:
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hook = models.URLField('URL for sending a TLE update notification')

    tles = models.ManyToManyField(tle.TLE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
