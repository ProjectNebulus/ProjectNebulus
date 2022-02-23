from dacite import from_dict


def encode_class(data, given_class):
    """
    Converts a dict into an instance of the given class.
    """
    return from_dict(data_class=given_class, data=data)
