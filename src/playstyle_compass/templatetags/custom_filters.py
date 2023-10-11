"""Custom filters."""


from django import template

register = template.Library()


@register.filter(name="format_category_label")
def format_category_label(category):
    """Format a category label for better display."""
    category_labels = {
        "gaming_history": "gaming history",
        "favorite_genres": "favorite genres",
        "preferred_platforms": "preferred platforms",
        "common_genres_platforms": "common preferences",
    }

    return category_labels.get(category, category.replace("_", " "))


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
    return value.split(", ")
