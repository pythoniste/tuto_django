from django.contrib import admin

from .models import Player, Game


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass
