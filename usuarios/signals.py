from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

@receiver(pre_save, sender=User)
def username_igual_email(sender, instance, **kwargs):
    user_email = instance.email
    username = user_email[:30]
    n = 1
    while User.objects.exclude(pk=instance.pk).filter(username=username).exists():
        n += 1
        username = user_email[:(29 - len(str(n)))] + '-' + str(n)
    instance.username = username