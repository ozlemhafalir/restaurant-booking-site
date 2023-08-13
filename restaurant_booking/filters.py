from django.template.defaultfilters import register


@register.filter(name="index_class")
def index_class(value):
    return "active" if value == 0 else ""


@register.filter(name="is_active")
def is_active(value, arg):
    return "active" if value == arg else ""


@register.filter(name="reservation_status_class")
def reservation_status_class(value):
    if value == "approved":
        return "success"
    elif value == "pending":
        return "secondary"
    elif value == "declined":
        return "danger"
    elif value == "cancelled":
        return "dark"
    else:
        return ""


@register.filter(name="restaurant_status_class")
def restaurant_status_class(value):
    if value == "approved":
        return "warning"
    elif value == "pending":
        return "secondary"
    elif value == "active":
        return "success"
        return ""


@register.filter(name="selected_if_in_list")
def selected_if_in_list(value, items):
    return "selected" if value in items else ""