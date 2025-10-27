from uuid import uuid4

from django.contrib.admin import ModelAdmin, TabularInline, register, HORIZONTAL, RelatedOnlyFieldListFilter, display, action
from django.db.models import BooleanField
from django.forms import CheckboxSelectMultiple, ChoiceField, ModelChoiceField
from django.utils.html import format_html
from django.utils.lorem_ipsum import sentence
from django.utils.translation import gettext_lazy as gettext

from .fields import CategoryChoiceField
from .widgets import NullBooleanRadioSelect


from .models import (
    Category,
    Mapping,
    Tag,
    Sticker,
    ColoredSticker,
    Theme,
    Test,
)


@register(Category)
class CategoryAdmin(ModelAdmin):
    search_fields = ("label",)


@register(Tag)
class TagAdmin(ModelAdmin):
    search_fields = ("label",)


@register(ColoredSticker)
class ColoredStickerAdmin(ModelAdmin):
    search_fields = ("label",)


@register(Sticker)
class StickerAdmin(ModelAdmin):
    search_fields = ("label",)


@register(Theme)
class ThemeAdmin(ModelAdmin):
    search_fields = ("label",)
    list_display = ("label", "color")


class MappingInline(TabularInline):
    model = Mapping
    autocomplete_fields = ("tag",)
    min_num = 0
    max_num = 3
    extra = 1


@register(Test)
class TestAdmin(ModelAdmin):

    fieldsets = (
        (None, {
            "fields": (
                ("label", "slug", "active"),
                ("owner", "url", "key", "highlight"),
                ("lorem",)
            )
        }),
        (gettext("Relations"), {
            "fields": (
                ("category", "theme_set"),
                ("category2", "theme_set2"),
                ("category3", "theme_set3"),
                ("category4", "theme_set4"),
                ("category5", "category6"),
                ("theme_set5", "theme_set6"),
            )
        }),
        (gettext("Numbers"), {
            "fields": (
                ("number", "percent", "progress", "grade"),
            )
        }),
        (gettext("Dates"), {
            "fields": (
                ("creation_date", "last_modification_date", "random_date"),
                ("creation_datetime", "last_modification_datetime", "random_datetime"),
                ("creation_time", "last_modification_time", "random_time"),
                ("duration",)
            )
        }),
        (gettext("IP"), {
            "fields": (
                ("ip", "ipv4", "ipv6_forced", "ipv6"),
            )
        }),
        (gettext("Uploads"), {
            "fields": (
                ("file", "image", "path"),
            )
        }),
    )
    readonly_fields = (
        "creation_date",
        "last_modification_date",
        "creation_datetime",
        "last_modification_datetime",
        "creation_time",
        "last_modification_time",
        "lorem",
    )

    prepopulated_fields = {
        "slug": ("label",),
    }
    autocomplete_fields = (
        "category2",
        "theme_set2",
    )
    radio_fields = {
        "category3": HORIZONTAL,
    }
    filter_horizontal = (
        "theme_set5",
    )
    filter_vertical = (
        "theme_set6",
    )
    inlines = [MappingInline]
    formfield_overrides = {
        BooleanField: {"widget": NullBooleanRadioSelect},
    }
    raw_id_fields = (
        "category4",
        "theme_set4",
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "theme_set3":
            kwargs.update({"widget": CheckboxSelectMultiple()})
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category5":
            return CategoryChoiceField(
                required=False,
                queryset=Category.objects.all().order_by(),
            )
        elif db_field.name == "category6":
            field = ModelChoiceField(
                required=False,
                queryset=Category.objects.filter(parent__parent__isnull=True)
            )
            field.choices = list(e for e in field.choices if not e[0]) + list(
                (
                    group.label, list(
                        (option.id, option.label)
                        for option in Category.objects.filter(parent=group)
                    )
                )
                for group in Category.objects.filter(parent__isnull=True)
            )
            return field
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    search_fields = ("label", "description")
    list_filter = (
        "category",
        ("category2", RelatedOnlyFieldListFilter),
    )
    list_display = (
        "number",
        "label",
        "highlight",
        "key",
        "go",
        "lorem",
    )
    list_display_links = ("key", "go")
    list_editable = (
        "number",
        "label",
    )

    @display(description=gettext("lorem ipsum sentence"))
    def lorem(self, obj):
        return format_html("<p>{}</p>", sentence())

    @display(description=gettext("lien vers la fiche"))
    def go(self, obj):
        return obj.label

    def action_message(self, request, rows_updated):
        if rows_updated == 0:
            self.message_user(request, gettext("No row updated"))
        elif rows_updated == 1:
            self.message_user(request, gettext("1 row updated"))
        else:
            self.message_user(request, gettext("{} rows updated").format(rows_updated))

    @action(description=gettext("Turn Highlight on"))
    def highlight_on(self, request, queryset):
        rows_updated = queryset.update(highlight=True)
        self.action_message(request, rows_updated)

    @action(description=gettext("Turn Highlight off"))
    def highlight_off(self, request, queryset):
        rows_updated = queryset.update(highlight=False)
        self.action_message(request, rows_updated)

    @action(description=gettext("Cancel Highlight"))
    def highlight_cancel(self, request, queryset):
        rows_updated = queryset.update(highlight=None)
        self.action_message(request, rows_updated)

    @action(description=gettext("Reset key"))
    def reset_key(self, request, queryset):
        for obj in queryset.all():
            obj.key = uuid4()
            obj.save()
        self.action_message(request, queryset.count())

    actions = [highlight_on, highlight_off, highlight_cancel, reset_key]
