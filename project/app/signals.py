from django.db.models.signals import  post_save
from django.dispatch import receiver

from .models import Player
from .tasks import create_avatar


@receiver(post_save, sender=Player)
def player_post_save_create_avatar(sender: type(Player), instance: Player, created: bool, **kwargs):
    if not instance.avatar:
        create_avatar.delay(instance.pk)
