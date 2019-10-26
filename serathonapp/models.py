from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement, AbstractBaseTag
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    married = models.BooleanField(default=False)
    age = models.IntegerField(blank=True, default=0)
    risk_level = models.SmallIntegerField(default=1)
    education = models.CharField(blank=True, max_length=50)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()