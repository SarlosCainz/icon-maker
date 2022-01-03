
def get_param(params, key, default):
    return params[key] if key in params else default


def get_int_param(params, key, default):
    return int(get_param(params, key, default))
