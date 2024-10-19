from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.contrib import admin
from django.utils.translation import gettext_lazy as gettext
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter

from .models import (
    Player,
    Guest,
    Subscriber,
    TeamMate,
    GameMaster,
    Game,
    Question,
    Answer,
    Play,
)

from .filters import (
    CreationMonthListFilter,
    ModificationMonthListFilter,
    SubscriptionMonthListFilter,
)

from .views import GamePlayView


class PlayerChildAdmin(PolymorphicChildModelAdmin):
    base_model = Player

    base_search_fields = ("user__username", "user__first_name", "user__last_name", "description")
    base_list_filter = (
        "profile_activated",
        "subscription_date",
        "score",
        CreationMonthListFilter,
        ModificationMonthListFilter,
        SubscriptionMonthListFilter,
    )
    base_list_display = (
        "user_username",
        "user_first_name",
        "user_last_name",
        "avatar",
        "profile_activated",
        "description",
        "subscription_date",
        "score",
    )
    base_list_display_links = (
        "user_username",
        "user_first_name",
        "user_last_name",
    )
    base_list_editable = ("description", "profile_activated")

    base_fieldsets = (
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
                ("description",),
                ("score",),
            )
        }),
    )
    readonly_fields = ("creation_datetime", "last_modification_datetime")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            readonly_fields += ("user",)
        return readonly_fields

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = gettext("username")

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = gettext("first name")

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = gettext("last name")

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def action_message(self, request, rows_updated):
        if rows_updated == 0:
            self.message_user(request, gettext("No row updated"))
        elif rows_updated == 1:
            self.message_user(request, gettext("1 row updated"))
        else:
            self.message_user(request, gettext("{} rows updated").format(rows_updated))

    def reset_scores(self, request, queryset):
        rows_updated = queryset.update(score=0)
        self.action_message(request, rows_updated)
    reset_scores.short_description = gettext("Reset scores")

    actions = [reset_scores]


@admin.register(Guest)
class GuestAdmin(PlayerChildAdmin):
    base_model = Guest
    fieldsets = (
        (gettext("Invitation"), {
            "fields": (
                ("invited_by",),
            )
        }),
    )

    def get_fieldsets(self, request, obj=None) -> tuple:
        """Permet de rajouter automatiquement les champs spécifiques des modèles de référence."""
        return self.base_fieldsets + self.fieldsets


@admin.register(Subscriber)
class SubscriberAdmin(PlayerChildAdmin):
    base_model = Subscriber


@admin.register(TeamMate)
class TeamMateAdmin(PlayerChildAdmin):
    base_model = TeamMate

    def has_module_permission(self, request):
        return False

@admin.register(GameMaster)
class GameMasterAdmin(PlayerChildAdmin):
    base_model = GameMaster
    show_in_index = True


@admin.register(Player)
class PlayerParentAdmin(PolymorphicParentModelAdmin):
    base_model = Player
    child_models = (Guest, Subscriber, TeamMate, GameMaster)
    list_filter = (PolymorphicChildModelFilter, )


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ("text", "points", "order")
    min_num = 2
    max_num = 5
    extra = 1



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    fields = ("text", "points")

    def has_module_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_save_and_add_another'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)

    def _response_post_save(self, request, obj):
        post_url = reverse("admin:app_game_change", kwargs={"object_id": obj.game.pk})
        preserved_filters = self.get_preserved_filters(request)
        post_url = add_preserved_filters(
            {"preserved_filters": preserved_filters, "opts": self.opts}, post_url
        )
        return HttpResponseRedirect(post_url)


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ("text", "points", "set_of_answers", "order")
    readonly_fields = ("set_of_answers", )
    min_num = 2
    max_num = 5
    extra = 1
    show_change_link = True

    @admin.display(description="Answers")
    def set_of_answers(self, obj):
        data = "</li><li>".join(str(answer) for answer in obj.answer_set.all())
        return mark_safe(f"<ul><li>{data}</li></ul>")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    search_fields = (
        "name",
        "duration",
        "level",
    )
    list_filter = (
        "status",
    )
    list_display = (
        "name",
        "status",
        "duration",
        "level",
        "link",
        "play",
    )
    list_display_links = (
        "link",
    )
    list_editable = ("name", "status", "duration", "level")
    readonly_fields = ("link",)

    fieldsets = (
        (None, {
            "fields": (
                ("name", "status",),
                ("duration", "level"),
            )
        }),
    )

    def link(self, obj):
        return gettext("Open")

    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            Answer.objects.bulk_create(
                Answer(
                    question=question,
                    text="TODO",
                )
                for question in obj.question_set.all()
            )

    def get_urls(self):
        return [
            path(
                "<path:pk>/play/",
                self.admin_site.admin_view(GamePlayView.as_view()),
                name="game_play",
            ),
            *super().get_urls(),
        ]

    def play(self, obj):
        url = reverse("admin:game_play", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')


class EntryInline(admin.TabularInline):
    model = Play.entry_set.through
    fields = ("answer",)
    min_num = 2
    max_num = 5
    extra = 1


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):

    fields = ("player", "game")

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return True
        return obj.player.user == request.user

    def has_change_permission(self, request, obj=None):
        return self.has_view_permission(request, obj)

    def has_add_permission(self, request):
        return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "player" and not request.user.is_superuser:
            field.queryset = field.queryset.filter(user=request.user)
        return field

    inlines = [EntryInline]
