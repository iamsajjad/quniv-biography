
from functools import lru_cache

from django.db.models import Q


@lru_cache(maxsize=512)
def text(query):

    return Q(Q(first_name__icontains=query) | Q(last_name__icontains=query) |
           Q(third_name__icontains=query) | Q(surname__icontains=query) |
           Q(field_here__icontains=query))

