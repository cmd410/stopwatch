
data = 'world'


def st_format_with_mapping():
    return 'Hello, {data}'.format(data=data)


def st_format_without_mapping():
    return 'Hello, {}'.format(data)


def st_f_string():
    return f'Hello, {data}!'


def st_concantenation():
    return 'Hello, ' + data + '!'


def st_percent_formating_with_mapping():
    return 'Hello, %(data)s!' % {'data': data}

def st_percent_format_without_mapping():
    return 'Hello, %s!' % data