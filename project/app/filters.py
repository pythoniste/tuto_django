from datetime import date

from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as gettext


class QuestionQuantityFilter(SimpleListFilter):
    """
    This objects allow to filter actions according to the number of questions
    """
    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = gettext("Quizz length")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "question_quantity"

    def lookups(self, request, model_admin):
        return (
            ("0", gettext("Void")),
            ("1-10", gettext("Quick")),
            ("11-25", gettext("Medium")),
            ("26-inf", gettext("Long")),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset

        q_min = q_max = None
        match value:
            case "0":
                q_min = q_max = 0
            case "1-10":
                q_min, q_max = 1, 10
            case "11-25":
                q_min, q_max = 11, 25
            case "26-inf":
                q_min, q_max = 26, None

        if q_min is not None:
            queryset = queryset.filter(nb_questions__gte=q_min)
        if q_max is not None:
            queryset = queryset.filter(nb_questions__lte=q_max)

        return queryset


def list_filter_factory(field_name: str, title: str, parameter_name: str, duration_unit: str) -> type:
    """## Month / Year filter factory"""
    class CustomListFilter(SimpleListFilter):
        """
        Month or Year filter for some action's attributes used for list IHM

        This objects allow to filter actions according to any month effectively used in at least one action.
        This is an action specific filter.
        """

        def lookups(self, request, model_admin):
            """Generator that get used months or years and format it"""
            label_format = "%Y" if duration_unit == "year" else "%B %Y"
            for month in model_admin.get_queryset(request).dates(field_name, duration_unit, order="DESC"):
                yield (month.strftime("%m-%Y"), month.strftime(label_format))

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

                return queryset.filter(
                    **{
                        f"{field_name}__gte": date(start_year, start_month, 1),
                        f"{field_name}__lt": date(end_year, end_month, 1),
                    }
                )
            elif duration_unit == "year":
                return queryset.filter(
                    **{
                        f"{field_name}__gte": date(start_year, 1, 1),
                        f"{field_name}__lt": date(start_year, 12, 1),
                    }
                )

            return queryset

    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    CustomListFilter.title = title

    # Parameter for the filter that will be used in the URL query.
    CustomListFilter.parameter_name = parameter_name

    return CustomListFilter


CreationMonthListFilter = list_filter_factory(
    "created_at", gettext("creation month"), "creation_month", "month")
ModificationMonthListFilter = list_filter_factory(
    "updated_at", gettext("last modification month"), "last_modification_month", "month")
SubscriptionMonthListFilter = list_filter_factory(
    "subscription_date", gettext("subscription month"), "subscription_month", "month")

CreationYearListFilter = list_filter_factory(
    "created_at", gettext("creation year"), "creation_year", "year")
ModificationYearListFilter = list_filter_factory(
    "updated_at", gettext("last modification year"), "last_modification_year", "year")
SubscriptionYearListFilter = list_filter_factory(
    "subscription_date", gettext("subscription year"), "subscription_year", "year")
