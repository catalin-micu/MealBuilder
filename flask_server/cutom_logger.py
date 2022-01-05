import logging


def create_logger(name: str, form: str):
    """
    creates custom logger object
    :param name: name of the logger (convention to use __name__ when the function is called)
    :param form: shape of the logged messages
    :return: logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(form)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger