def _pad_with_zero(numeric_value):
    if numeric_value < 10:
        return "0%d" % (numeric_value)
    else:
        return "%d" % (numeric_value)


def hms_format(initial_seconds):
    hours = 0
    minutes, seconds = divmod(initial_seconds, 60)
    if minutes >= 60:
        hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return "%s:%s:%s" % (_pad_with_zero(hours), _pad_with_zero(minutes),
                             _pad_with_zero(seconds))
    else:
        return "%s:%s" % (_pad_with_zero(minutes),  _pad_with_zero(seconds))
