from django import template

register = template.Library()

@register.filter
def humanise_duration(value):
    if not value:
        return ""
    # Convert total seconds to hours, minutes, and seconds
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0 and minutes != 0:
        return f"{hours} hrs {minutes} mins"
    elif hours >= 1 and minutes == 0:
        return f"{hours} hrs"
    elif minutes > 0:
        return f"{minutes} mins"
    else:
        return f"{seconds} secs"
