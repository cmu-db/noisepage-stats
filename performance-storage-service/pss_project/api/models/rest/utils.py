def to_dict(obj):
    """ Recursively turn an object to a Python dict """
    data = {}
    for key, value in obj.__dict__.items():
        try:
            data[key] = to_dict(value)
        except AttributeError:
            data[key] = value
    return data
