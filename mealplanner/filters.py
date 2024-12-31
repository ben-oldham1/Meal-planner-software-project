from .models import DIFFICULTY_CHOICES, Recipe, Tag, Ingredient
import django_filters

class RecipeFilter(django_filters.FilterSet):
    # difficulty = ChoiceFilter(choices=DIFFICULTY_CHOICES)
    #time_needed = django_filters.DurationFilter()

    o = django_filters.OrderingFilter(
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
        fields = ['difficulty', 'time_needed', 'tags']