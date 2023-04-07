from functools import reduce
from django.db.models import Q

class PropertyFilterStrategy:
    def __init__(self, name):
        self.name = name

    def apply(self, queryset, value):
        pass

class KeywordsFilter(PropertyFilterStrategy):
    def apply(self, queryset, value):
        if value:
            queryset = queryset.filter(Q(project_Title__icontains=value) | Q(street__icontains=value))
        return queryset

class PropertyTypeFilter(PropertyFilterStrategy):
    def apply(self, queryset, value):
        if value != '' and value != 'All':
            queryset = queryset.filter(propertyType__iexact=value)
        return queryset

class BedroomsFilter(PropertyFilterStrategy):
    def apply(self, queryset, value):
        if value != '' and value != 'All':
            queryset = queryset.filter(bedrooms__lte=value)
        return queryset

class PriceFilter(PropertyFilterStrategy):
    def apply(self, queryset, value):
        if value != '' and value != 'All':
            if value != '10001':
                queryset = queryset.filter(rent__lte=value)
            else:
                queryset = queryset.filter(rent__gt=10000)
        return queryset

class AreaFilter(PropertyFilterStrategy):
    def apply(self, queryset, value):
        if value != 'All' and value != '':
            if value != '5001':
                queryset = queryset.filter(sqft__lte=int(value))
            else:
                queryset = queryset.filter(sqft__gt=5000)
        return queryset

def apply_filters(queryset, params):
    strategies = [
        KeywordsFilter('keywords'),
        PropertyTypeFilter('property_type'),
        BedroomsFilter('bedrooms'),
        PriceFilter('price'),
        AreaFilter('area'),
    ]
    
    return combined_filters(*strategies)(queryset, params)

def combined_filters(*strategies):
    def apply(queryset, values):
        return reduce(lambda acc, strategy: strategy.apply(acc, values.get(strategy.name, '')), strategies, queryset)
    return apply