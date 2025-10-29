from django.contrib.admin.templatetags.admin_list import pagination
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.template import Library
from django.template.base import Parser, Token
from django.urls import reverse_lazy
from django.utils.html import format_html

from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon


__all__ = [
    "icon_action",
    "pagination_tag",
]


register = Library()


ICONS = {
    "list": "list-columns-reverse",
    "create": "plus",
    "detail": "eye",
    "update": "pencil",
    "delete": "trash",
    "bulk_create_qr": "database-add",
}


@register.simple_tag
def icon_action(page, pk=None):
    if pk is None:
        return format_html(
            """<a href="{}" class="border">{}</a>""",
            reverse_lazy(f"game:{page}"),
            bs_icon(ICONS[page]),
        )
    return format_html(
        """<a href="{}" class="border">{}</a>""",
        reverse_lazy(f"game:{page}", kwargs={"pk": pk}),
        bs_icon(ICONS[page]),
    )


@register.tag(name="pagination_top")
def pagination_tag(parser: Parser, token: Token) -> InclusionAdminNode:
    """Used to show pagination at the top of the table."""
    return InclusionAdminNode(
        parser,
        token,
        func=pagination,
        template_name="pagination_top.html",
        takes_context=False,
    )

