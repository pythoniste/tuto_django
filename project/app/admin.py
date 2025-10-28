from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as gettext

from mptt.admin import MPTTModelAdmin

from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)

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
    Genre,
    StatGame,
)

from .filters import (
    QuestionQuantityFilter,
    CreationMonthListFilter,
    ModificationMonthListFilter,
    SubscriptionMonthListFilter,
    CreationYearListFilter,
    ModificationYearListFilter,
    SubscriptionYearListFilter,
)


class PlayerChildAdmin(PolymorphicChildModelAdmin):
    base_model = Player
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
        "polymorphic_ctype_name",
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
    base_fieldsets = (
        (None, {
            "fields": (
                ("user", "avatar",),
                ("created_at", "updated_at"),
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
    fieldsets = ()
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj is not None:
            readonly_fields += ("user",)
        return readonly_fields

    def get_fieldsets(self, request, obj=None) -> tuple:
        return self.base_fieldsets + self.fieldsets

    @admin.display(description=gettext("username"))
    def user_username(self, obj):
        return obj.user.username

    @admin.display(description=gettext("first name"))
    def user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description=gettext("last name"))
    def user_last_name(self, obj):
        return obj.user.last_name

    @admin.display(description=gettext("Type"))
    def polymorphic_ctype_name(self, obj):
        return obj.polymorphic_ctype.name.capitalize()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "user":
            formfield.queryset = formfield.queryset.filter(player__isnull=True)
        return formfield

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def action_message(self, request, rows_updated):
        if rows_updated == 0:
            self.message_user(request, gettext("No row updated"))
        elif rows_updated == 1:
            self.message_user(request, gettext("1 row updated"))
        else:
            self.message_user(request, gettext("{} rows updated").format(rows_updated))

    @admin.action(description=gettext("Reset scores"))
    def reset_scores(self, request, queryset):
        rows_updated = queryset.update(score=0)
        self.action_message(request, rows_updated)

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


@admin.register(Subscriber)
class SubscriberAdmin(PlayerChildAdmin):
    base_model = Subscriber
    fieldsets = (
        (gettext("Subscription details"), {
            "fields": (
                ("registration_date", "sponsor"),
            )
        }),
    )


@admin.register(TeamMate)
class TeamMateAdmin(PlayerChildAdmin):
    base_model = TeamMate
    fieldsets = (
        (gettext("Membership details"), {
            "fields": (
                ("registration_date", "team_member_date"),
            )
        }),
    )


@admin.register(GameMaster)
class GameMasterAdmin(PlayerChildAdmin):
    base_model = GameMaster
    show_in_index = True
    fieldsets = (
        (gettext("Membership details"), {
            "fields": (
                ("registration_date", "team_member_date"),
            )
        }),
    )


@admin.register(Player)
class PlayerParentAdmin(PolymorphicParentModelAdmin):
    base_model = Player
    child_models = (Guest, Subscriber, TeamMate, GameMaster)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    list_filter = (
        PolymorphicChildModelFilter,
        "profile_activated",
        "subscription_date",
        "score",
        CreationMonthListFilter,
        ModificationMonthListFilter,
        SubscriptionMonthListFilter,
        CreationYearListFilter,
        ModificationYearListFilter,
        SubscriptionYearListFilter,
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

    @admin.display(description=gettext("username"))
    def user_username(self, obj):
        return obj.user.username

    @admin.display(description=gettext("first name"))
    def user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description=gettext("last name"))
    def user_last_name(self, obj):
        return obj.user.last_name

    def action_message(self, request, rows_updated):
        if rows_updated == 0:
            self.message_user(request, gettext("No row updated"))
        elif rows_updated == 1:
            self.message_user(request, gettext("1 row updated"))
        else:
            self.message_user(request, gettext("{} rows updated").format(rows_updated))

    @admin.action(description=gettext("Reset scores"))
    def reset_scores(self, request, queryset):
        rows_updated = queryset.update(score=0)
        self.action_message(request, rows_updated)

    actions = [reset_scores]


class QuestionInline(admin.TabularInline):
    model = Question
    fields = ("text", "points", "set_of_answers", "order")
    readonly_fields = ("set_of_answers",)
    min_num = 2
    max_num = 50
    extra = 1
    show_change_link = True

    @admin.display(description="Answers")
    def set_of_answers(self, obj):
        return format_html(
            "<ul><li>{}</li></ul>",
            mark_safe("</li><li>".join(str(answer) for answer in obj.answer_set.all())),
        )


@admin.register(Genre)
class GenreAdmin(MPTTModelAdmin):

    mptt_level_indent = 20


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
        "created_at",
        "updated_at",
    )

    def link(self, obj):
        return gettext("Open")

    fieldsets = (
        (None, {
            "fields": (
                ("name", "status",),
                ("duration", "level"),
                ("created_at", "updated_at"),
            )
        }),
    )
    inlines = [QuestionInline]
    def get_inlines(self, request, obj):
        if obj is None:
            return []
        return super().get_inlines(request, obj)


class AnswerInline(admin.TabularInline):
    model = Answer
    fields = ("text", "points", "order")
    min_num = 2
    max_num = 5
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = (
        "text",
        "points",
    )
    inlines = [AnswerInline]

    def has_module_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_save_and_add_another'] = extra_context['show_delete'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)

    def _response_post_save(self, request, obj):
        if self.has_view_or_change_permission(request):
            post_url = reverse("admin:app_game_change", kwargs={"object_id": obj.game.pk})
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": self.opts}, post_url
            )
        else:
            post_url = reverse("admin:index", current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


class EntryInline(admin.TabularInline):
    model = Play.entry_set.through
    fields = ("answer",)
    min_num = 2
    max_num = 5
    extra = 1


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
    inlines = [EntryInline]

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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(player__user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "player" and not request.user.is_superuser:
            formfield.queryset = formfield.queryset.filter(user=request.user)
            formfield.initial = Player.objects.get(user=request.user)
        return formfield


@admin.register(StatGame)
class StatGameAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )
    list_filter = (
        "status",
        "level",
        QuestionQuantityFilter,
    )
    list_display = (
        "name",
        "status",
        "duration",
        "level",
        "nb_questions",
        "nb_players",
    )
    readonly_fields = (
        "nb_questions",
        "nb_players",
    )
    list_display_links = None

    @admin.display(description=gettext("Number of questions"))
    def nb_questions(self, obj):
        # return obj.question_set.count()
        return obj.nb_questions

    @admin.display(description=gettext("Number of players"))
    def nb_players(self, obj):
        return obj.nb_players

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
