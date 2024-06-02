"""Custom filters."""

import re
from datetime import datetime
from django import template
from itertools import zip_longest
from django.utils.translation import gettext as _
from django.apps import apps
from pytz import timezone
from django.utils import timezone as django_timezone
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name="format_category_label")
def format_category_label(category):
    """Format a category label for better display."""
    category_labels = {
        "gaming_history": _("gaming history"),
        "favorite_genres": _("favorite genres"),
        "themes": _("favorite themes"),
        "preferred_platforms": _("preferred platforms"),
        "common_genres_platforms": _("common preferences"),
    }

    return category_labels.get(category, _(category.replace("_", " ")))


@register.filter(name="getattr")
def getattr_filter(obj, attr_name):
    """Get an attribute of an object with optional attribute name filtering."""
    if attr_name == "preferred_platforms":
        attr_name = "platforms"
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return ""


@register.filter(name="split_by_comma")
def split_by_comma(value):
    """Split a string by commas and return a list."""
    if value:
        return value.split(", ")


@register.filter(name="is_favorite")
def is_favorite(game_id, user_favorites):
    if str(game_id) in user_favorites.split(","):
        return True
    return False


@register.filter(name="in_queue")
def in_queue(game_id, user_queue):
    if str(game_id) in user_queue.split(","):
        return True
    return False


@register.filter
def pluralize_reviews(count):
    return "review" if count == 1 else "reviews"


@register.filter(name="template_trans")
def template_trans(text):
    try:
        return _(text)
    except Exception:
        return text


@register.filter
def get_object_id(object_name, model_name):
    """
    Given an object name and a model, return the ID if it exists.
    """
    model = apps.get_model(app_label="playstyle_compass", model_name=model_name)
    try:
        if model_name == "Character":
            objs = model.objects.filter(name=object_name)
        else:
            objs = model.objects.filter(title=object_name)

        if objs.exists():
            if model_name == "Game":
                return objs.first().guid
            elif objs.count() == 1:
                return objs.first().id
            else:
                return [obj.id for obj in objs]
        else:
            return None
    except ObjectDoesNotExist:
        return None


@register.filter
def split_commas(value):
    return [item.strip() for item in value.split(",")]


@register.filter
def check_platform(platform, user_platforms):
    """Filter to check if a platform is present in the user preferences."""
    # Note:
    """This filter is used because checking with the "in" operator
    always returns True for the 'PlayStation' platform when the user has 
    'PlayStation 5' or 'PlayStation 4' in their preferrences."""
    if not "," in user_platforms:
        return platform == user_platforms
    else:
        return platform in user_platforms


@register.filter
def convert_to_user_timezone(timestamp, user_timezone):
    timestamp = django_timezone.localtime(timestamp)
    user_tz = timezone(user_timezone)
    timestamp_in_user_tz = timestamp.astimezone(user_tz)
    formatted_timestamp = timestamp_in_user_tz.strftime("%B %d, %Y, %I:%M %p")

    return formatted_timestamp


@register.filter
def bold_requirements(value):
    """Filter used to make requirements in bold."""
    if value:
        requirements = [
            "Processor:",
            "OS:",
            "OS \\*:",
            "Memory:",
            "Graphics:",
            "DirectX:",
            "Storage:",
            "Sound Card:",
            "Additional Notes:",
        ]
        for req in requirements:
            value = re.sub(f"({req})", r"<strong>\1</strong>", value)

        return mark_safe(value)
    return None
