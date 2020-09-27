def convert_environment_to_dict(environment):
    db_formatted_environment = {
        'os_version': environment.os_version,
        'cpu_number': environment.cpu_number,
        'cpu_socket': environment.cpu_socket
    }
    return db_formatted_environment
