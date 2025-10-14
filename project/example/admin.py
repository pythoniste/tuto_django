from django.contrib.admin import ModelAdmin, register

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
    pass


@register(Mapping)
class MappingAdmin(ModelAdmin):
    pass


@register(Tag)
class TagAdmin(ModelAdmin):
    pass


@register(ColoredSticker)
class ColoredStickerAdmin(ModelAdmin):
    pass


@register(Sticker)
class StickerAdmin(ModelAdmin):
    pass


@register(Theme)
class ThemeAdmin(ModelAdmin):
    pass


@register(Test)
class TestAdmin(ModelAdmin):
    pass
