from functools import partial
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    Model,
    CharField,
    EmailField,
    URLField,
    UUIDField,
    SlugField,
    TextField,
    BooleanField,
    DateField,
    DateTimeField,
    TimeField,
    PositiveSmallIntegerField,
    GenericIPAddressField,
    DurationField,
    DecimalField,
    FloatField,
    IntegerField,
    BinaryField,
    FilePathField,
    FileField,
    ImageField,
    ForeignKey,
    ManyToManyField,
    CASCADE,
    PROTECT,
    Index,
    UniqueConstraint,
)
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as gettext

from .enums import StickerCategory


def compute_upload_path(current_object, filename, sub_path):
    """Describe the image storage path"""
    today = now()
    return str(
        Path.joinpath(
            *list(
                map(
                    Path,
                    (
                        current_object._meta.app_label,  # pylint: disable=protected-access
                        current_object._meta.model_name,  # pylint: disable=protected-access
                        sub_path,
                        str(today.year),
                        str(today.month),
                        str(uuid4()) + Path(filename).suffix
                    )
                )
            )
        )
    )


class Tag(Model):

    label = CharField(
        verbose_name=gettext("menu label"),
        help_text=gettext("used in the menu when fully deployed"),
        max_length=127,
        blank=False,
        db_index=True,
        unique=True,
    )

    def __str__(self):
        """Return a string that represent the current object to an end user."""
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Tag Meta class"""

        verbose_name = gettext("tag")
        verbose_name_plural = gettext("tags")
        ordering = ("label",)


class Sticker(Model):

    label = CharField(
        verbose_name=gettext("label"),
        max_length=127,
        blank=False,
        db_index=True,
    )

    category = CharField(
        verbose_name=gettext("category"),
        choices=StickerCategory,
        max_length=8,
        blank=False,
        db_index=True,
    )

    def __str__(self):
        """Return a string that represent the current object to an end user."""
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Tag Meta class"""

        verbose_name = gettext("sticker")
        verbose_name_plural = gettext("stickers")
        ordering = ("category", "label")
        indexes = [
            Index(
                fields=["category", "label"],
                name="sticker_main_index"),
        ]
        constraints = [
            UniqueConstraint(
                fields=["category", "label"],
                name="sticker_unicity_constraint"
            ),
        ]


class ColoredSticker(Sticker):

    color = CharField(
        verbose_name=gettext("color"),
        max_length=7,
        blank=False,
        db_index=True,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Tag Meta class"""

        verbose_name = gettext("colored sticker")
        verbose_name_plural = gettext("colored stickers")


class Theme(Model):

    COLORS = (
        ("#ffffff", gettext("White")),
        ("#ff0000", gettext("Red")),
        ("#00ff00", gettext("Green")),
        ("#0000ff", gettext("Blue")),
        ("#000000", gettext("Black")),
    )

    label = CharField(
        verbose_name=gettext("label"),
        max_length=127,
        blank=False,
        db_index=True,
        unique=True,
    )

    color = CharField(
        verbose_name=gettext("color"),
        choices=COLORS,
        max_length=7,
        blank=False,
        db_index=True,
        unique=True,
    )

    def __str__(self):
        """Return a string that represent the current object to an end user."""
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Theme Meta class"""

        verbose_name = gettext("theme")
        verbose_name_plural = gettext("themes")
        ordering = ("label",)


class Category(Model):

    parent = ForeignKey(
        verbose_name=gettext("parent"),
        related_name="child_set",
        to="self",
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    label = CharField(
        verbose_name=gettext("label"),
        max_length=127,
        blank=False,
        db_index=True,
        unique=True,
    )

    @property
    def depth(self):
        if self.parent_id:
            return self.parent.depth + 1
        return 0

    @property
    def full_label(self):
        if self.parent_id:
            return self.parent.full_label + " > " + self.label
        return self.label

    @property
    def deep_label(self):
        return "\u2003" * ((self.depth - 1) * 2 - 1) + (self.depth and "\u2514\u2500" or "") + self.label

    def __str__(self):
        """Return a string that represent the current object to an end user."""
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Category Meta class"""

        verbose_name = gettext("category")
        verbose_name_plural = gettext("categories")
        ordering = ("label",)


class Test(Model):

    id = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    label = CharField(
        verbose_name=gettext("label"),
        max_length=32,
        blank=False,
        db_index=True,
        unique=True,
    )

    category = ForeignKey(
        verbose_name=gettext("category"),
        related_name="test_set",
        to=Category,
        null=True,
        blank=True,
        db_index=True,
        on_delete=PROTECT,
    )

    theme_set = ManyToManyField(
        verbose_name=gettext("theme_set"),
        related_name="test_set",
        to=Theme,
        blank=True,
    )

    category2 = ForeignKey(
        verbose_name=gettext("category 2"),
        related_name="test2_set",
        to=Category,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    theme_set2 = ManyToManyField(
        verbose_name=gettext("theme_set 2"),
        related_name="test2_set",
        to=Theme,
        blank=True,
    )

    category3 = ForeignKey(
        verbose_name=gettext("category 3"),
        related_name="test3_set",
        to=Category,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    theme_set3 = ManyToManyField(
        verbose_name=gettext("theme_set 3"),
        related_name="test3_set",
        to=Theme,
        blank=True,
    )

    category4 = ForeignKey(
        verbose_name=gettext("category 4"),
        related_name="test4_set",
        to=Category,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    theme_set4 = ManyToManyField(
        verbose_name=gettext("theme_set 4"),
        related_name="test4_set",
        to=Theme,
        blank=True,
    )

    category5 = ForeignKey(
        verbose_name=gettext("category 5"),
        related_name="test5_set",
        to=Category,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    theme_set5 = ManyToManyField(
        verbose_name=gettext("theme_set 5"),
        related_name="test5_set",
        to=Theme,
        blank=True,
    )

    category6 = ForeignKey(
        verbose_name=gettext("category 6"),
        related_name="test6_set",
        to=Category,
        null=True,
        blank=True,
        db_index=True,
        on_delete=CASCADE,
    )

    theme_set6 = ManyToManyField(
        verbose_name=gettext("theme_set 6"),
        related_name="test6_set",
        to=Theme,
        blank=True,
    )

    tag_set = ManyToManyField(
        verbose_name=gettext("theme_set"),
        related_name="test_set",
        to=Tag,
        through="Mapping",
        blank=True,
    )

    color = ForeignKey(
        verbose_name=gettext("Sticker color"),
        related_name="color_set",
        to=Sticker,
        limit_choices_to={"category": "color"},
        null=True,
        blank=True,
        on_delete=CASCADE,
    )

    quality = ForeignKey(
        verbose_name=gettext("Sticker quality"),
        related_name="quality_set",
        to=Sticker,
        limit_choices_to={"category": "quality"},
        null=True,
        blank=True,
        on_delete=CASCADE,
    )

    size = ForeignKey(
        verbose_name=gettext("Sticker size"),
        related_name="size_set",
        to=Sticker,
        limit_choices_to={"category": "size"},
        null=True,
        blank=True,
        on_delete=CASCADE,
    )

    number = PositiveSmallIntegerField(
        verbose_name=gettext("number"),
        unique=True,
    )

    percent = DecimalField(
        verbose_name=gettext("percent"),
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
    )

    progress = FloatField(
        verbose_name=gettext("progress"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True,
        null=True,
    )

    grade = IntegerField(
        verbose_name=gettext("grade"),
        validators=[MinValueValidator(-10), MaxValueValidator(10)],
        blank=True,
        null=True,
    )

    slug = SlugField(
        unique=True,
        max_length=32,
        editable=True,
        db_index=True,
    )

    owner = EmailField(
        verbose_name=gettext("owner"),
        blank=True,
        null=True,
    )

    url = URLField(
        verbose_name=gettext("url"),
        blank=True,
        null=True,
    )

    key = UUIDField(
        default=uuid4,
    )

    description = TextField(
        verbose_name=gettext("description"),
        blank=True,
    )

    active = BooleanField(
        verbose_name=gettext("active"),
    )

    highlight = BooleanField(
        verbose_name=gettext("highlight"),
        null=True,
        blank=True,
    )

    creation_date = DateField(
        verbose_name=gettext("creation date"),
        auto_now_add=True,
    )

    last_modification_date = DateField(
        verbose_name=gettext("last modification date"),
        auto_now=True,
    )

    random_date = DateField(
        verbose_name=gettext("random date"),
        blank=True,
        null=True,
    )

    creation_datetime = DateTimeField(
        verbose_name=gettext("creation datetime"),
        auto_now_add=True,
    )

    last_modification_datetime = DateTimeField(
        verbose_name=gettext("last modification datetime"),
        auto_now=True,
    )

    random_datetime = DateTimeField(
        verbose_name=gettext("random datetime"),
        blank=True,
        null=True,
    )

    duration = DurationField(
        verbose_name=gettext("duration"),
        blank=True,
        null=True,
    )

    creation_time = TimeField(
        verbose_name=gettext("creation time"),
        auto_now_add=True,
    )

    last_modification_time = TimeField(
        verbose_name=gettext("last modification time"),
        auto_now=True,
    )

    random_time = TimeField(
        verbose_name=gettext("random time"),
        blank=True,
        null=True,
    )

    ip = GenericIPAddressField(
        verbose_name=gettext("IP v4 or 6"),
        protocol="both",
        blank=True,
        null=True,
    )

    ipv4 = GenericIPAddressField(
        verbose_name=gettext("IP v4 as is"),
        protocol="IPv4",
        blank=True,
        null=True,
    )

    ipv6_forced = GenericIPAddressField(
        verbose_name=gettext("IP v6 (ipv4 will be converted)"),
        protocol="both",
        unpack_ipv4=True,
        blank=True,
        null=True,
    )

    ipv6 = GenericIPAddressField(
        verbose_name=gettext("IP v6"),
        protocol="IPv6",
        blank=True,
        null=True,
    )

    raw_data = BinaryField(
        verbose_name=gettext("raw data"),
        max_length=127,
        blank=True,
        null=True,
    )

    file = FileField(
        verbose_name=gettext("file"),
        max_length=256,
        upload_to=partial(compute_upload_path, subpath="file"),
        null=True,
        blank=True,
    )

    image = ImageField(
        verbose_name=gettext("image"),
        max_length=256,
        upload_to=partial(compute_upload_path, subpath="image"),
        null=True,
        blank=True,
    )

    path = FilePathField(
        verbose_name=gettext("path"),
        path=settings.STATIC_ROOT,
    )

    def __str__(self):
        """Return a string that represent the current object to an end user."""
        return self.label

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("test")
        verbose_name_plural = gettext("tests")
        ordering = ("number", )


class Mapping(Model):

    test = ForeignKey(
        verbose_name=gettext("test"),
        related_name="mapping_set",
        to=Test,
        null=False,
        blank=False,
        db_index=True,
        on_delete=CASCADE,
    )

    tag = ForeignKey(
        verbose_name=gettext("tag"),
        related_name="mapping_set",
        to=Tag,
        null=False,
        blank=False,
        db_index=True,
        on_delete=CASCADE,
    )

    order = PositiveSmallIntegerField(
        verbose_name=gettext("order"),
        default=0,
    )

    info = CharField(
        verbose_name=gettext("additional information"),
        max_length=255,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Mapping Meta class"""

        verbose_name = gettext("mapping")
        verbose_name_plural = gettext("mappings")
        ordering = ("test", "tag", "order")
        indexes = [
            Index(fields=["test", "tag", "order"], name="mapping_natural_keys_idx"),
        ]
        constraints = [
            UniqueConstraint(
                fields=["test", "tag", "order"],
                name="mapping_natural_keys_uni_constraint"
            ),
        ]
