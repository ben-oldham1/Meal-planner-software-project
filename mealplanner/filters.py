from .models import DIFFICULTY_CHOICES, Recipe, Tag, Ingredient
from datetime import timedelta
import django_filters

class RecipeFilter(django_filters.FilterSet):

    time_category = django_filters.ChoiceFilter(
        choices=[
            ('under_30', 'Under 30 mins'),
            ('30_to_45', '30-45 mins'),
            ('over_45', 'Over 45 minutes'),
        ],
        method='filter_by_time_needed',
        label='Time Needed',
    )

    sort = django_filters.OrderingFilter(
        label='Sort by',

        # tuple-mapping retains order
        fields=(
            ('difficulty', 'difficulty'),
            ('time_needed', 'time_needed'),
        ),

        # labels do not need to retain order
        field_labels={
            'difficulty': 'Difficulty',
            'time_needed': 'Time Needed',
        }
    )

    class Meta:
        model = Recipe
        fields = ['difficulty', 'tags']

    def filter_by_time_needed(self, queryset, name, value):
        if value == 'under_30':
            return queryset.filter(time_needed__lt=timedelta(minutes=30))
        elif value == '30_to_45':
            return queryset.filter(time_needed__gte=timedelta(minutes=30), time_needed__lt=timedelta(minutes=45))
        elif value == 'over_45':
            return queryset.filter(time_needed__gte=timedelta(minutes=45))
        return queryset