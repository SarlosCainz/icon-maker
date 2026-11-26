
class InvalidParam(Exception):
    """フォームの値が不正。app.py が 400 に変換する (docs/validation.md V4)"""

    def __init__(self, param, reason):
        super().__init__("{}: {}".format(param, reason))
        self.param = param
        self.reason = reason


def get_param(params, key, default):
    return params[key] if key in params else default


def get_int_param(params, key, default, for_ios=0, for_web=0, *, minimum=None, maximum=None):
    raw = get_param(params, key, default)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise InvalidParam(key, "整数で指定する")

    # 範囲の検証は倍率をかける前の値に対して行う (docs/validation.md)
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise InvalidParam(key, range_reason(minimum, maximum))

    value *= 4 if for_ios else 2 if for_web else 1

    return value


def get_choice_param(params, key, default, choices):
    value = get_param(params, key, default)
    if value not in choices:
        raise InvalidParam(key, "指定できるのは次のいずれか: " + ", ".join(choices))

    return value


def range_reason(minimum, maximum):
    if minimum is not None and maximum is not None:
        return "{} 以上 {} 以下の整数で指定する".format(minimum, maximum)
    if minimum is not None:
        return "{} 以上の整数で指定する".format(minimum)

    return "{} 以下の整数で指定する".format(maximum)
