
def get_param(params, key, default):
    return params[key] if key in params else default


def get_int_param(params, key, default, for_ios=0, for_web=0):
    value = int(get_param(params, key, default))
    value *= 4 if for_ios else 2 if for_web else 1

    return value
