from django.contrib import admin
from django.utils.translation import gettext_lazy as gettext

from .models import Player, Game, Question, Answer, Play


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    list_filter = (
        "profile_activated",
        "subscription_date",
        "score",
    )
    list_display = (
        "user_username",
        "user_first_name",
        "user_last_name",
        "avatar",
        "profile_activated",
        "subscription_date",
        "score",
    )
    list_display_links = (
        "user_username",
        "user_first_name",
        "user_last_name",
    )
    list_editable = (
        "profile_activated",
    )
    fieldsets = (
        (None, {
            "fields": (
                ("user", "avatar",),
                ("creation_datetime", "last_modification_datetime"),
            )
        }),
        (gettext("Contract information"), {
            "fields": (
                ("profile_activated", "subscription_date"),
                ("signed_engagement",),
            )
        }),
        (gettext("Personal information"), {
            "fields": (
                ("score",),
            )
        }),
    )
    readonly_fields = (
        "creation_datetime",
        "last_modification_datetime",
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            readonly_fields += ("user",)
        return readonly_fields

    @admin.display(description=gettext("username"))
    def user_username(self, obj):
        return obj.user.username

    @admin.display(description=gettext("first name"))
    def user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description=gettext("last name"))
    def user_last_name(self, obj):
        return obj.user.last_name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "user":
            formfield.queryset = formfield.queryset.filter(player__isnull=True)
        return formfield


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "duration",
    )
    list_filter = (
        "status",
        "level",
    )
    list_display = (
        "name",
        "status",
        "duration",
        "level",
        "link",
    )
    list_display_links = (
        "link",
    )
    list_editable = (
        "name",
        "status",
        "duration",
        "level",
    )
    readonly_fields = (
        "link",
    )

    def link(self, obj):
        return gettext("Ouvrir")

    fieldsets = (
        (None, {
            "fields": (
                ("name", "status",),
                ("duration", "level"),
            )
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = (
        "text",
        "points",
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "game",
    )
    fields = (
        "player",
        "game",
    )
