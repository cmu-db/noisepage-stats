def convert_environment_to_dict(environment):
    db_formatted_environment = {
        'os_version': environment.os_version,
        'cpu_number': environment.cpu_number,
        'cpu_socket': environment.cpu_socket
    }
    return db_formatted_environment


def to_dict(obj):
    """
    Recursively turn an object to a Python dict
    """
    data = {}
    for key, value in obj.__dict__.items():
        try:
            data[key] = to_dict(value)
        except AttributeError:
            data[key] = value
    return data