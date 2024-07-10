from datetime import date

from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


def month_list_filter_factory(field_name: str, title: str, parameter_name: str, duration_unit: str) -> type:
    """## Month filter factory"""
    class MonthListFilter(SimpleListFilter):
        """
        Month filter for some action's attributes used for list IHM

        This objects allow to filter actions according to any month effectively used in at least one action.
        This is an action specific filter.
        """

        def lookups(self, request, model_admin):
            """Generator that get used months and format it"""
            for month in model_admin.get_queryset(request).dates(field_name, duration_unit, order="DESC"):
                yield (month.strftime("%m-%Y"), month.strftime("%B %Y"))

        def queryset(self, request, queryset):
            """Query set to get actually used months"""
            value = self.value()
            if value is None:
                return queryset

            try:
                start_month, start_year = map(int, value.split("-"))
            except ValueError:
                return queryset

            if duration_unit == "month":
                if start_month == 12:
                    end_month, end_year = 1, start_year + 1
                else:
                    end_month, end_year = start_month + 1, start_year

                return queryset.filter(date__gte=date(start_year, start_month, 1),
                                       date__lt=date(end_year, end_month, 1))

            return queryset

    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    MonthListFilter.title = title

    # Parameter for the filter that will be used in the URL query.
    MonthListFilter.parameter_name = parameter_name

    return MonthListFilter


CreationMonthListFilter = month_list_filter_factory(
    "creation_datetime", _("creation date"), "creation_date", "month")
ModificationMonthListFilter = month_list_filter_factory(
    "last_modification_datetime", _("last modification date"), "last_modification_date", "month")
SubscriptionMonthListFilter = month_list_filter_factory(
    "subscription_date", _("subscription date"), "subscription_date", "month")
