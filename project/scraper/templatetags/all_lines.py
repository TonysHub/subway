from django import template
from scraper.models import Stations

register = template.Library()


@register.inclusion_tag("scraper/dropdown.html")
def find_all_lines():
    all_lines = Stations.objects.values("line").distinct()
    return {"all_lines": all_lines}
