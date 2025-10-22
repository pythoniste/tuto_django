from django.db import models
from django.utils.translation import gettext_lazy as gettext


class OrderingMixin(models.Model):

    order = models.PositiveSmallIntegerField(
        verbose_name = gettext("order"),
        default = 0,
    )

    class Meta:
        abstract = True


class TrackingMixin(models.Model):
    created_at = models.DateTimeField(
        verbose_name=gettext("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=gettext("updated at"),
        auto_now=True,
    )

    class Meta:
        abstract = True
