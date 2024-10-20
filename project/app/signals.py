from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig

from .models import Player, Play, Entry
from .tasks import create_avatar


@receiver(post_save, sender=Player)
def player_post_save_create_avatar(sender: AppConfig, instance: Player, created: bool, **kwargs):
    if not instance.avatar:
        create_avatar.delay(instance.pk)


@receiver(post_save, sender=Play)
def player_post_save_create_avatar(sender: AppConfig, instance: Play, created: bool, **kwargs):
    if instance.entry_set.count() == 0:
        Entry.objects.bulk_create(
            [
                Entry(play=instance, question=question)
                for question in instance.game.question_set.all()
            ]
        )
