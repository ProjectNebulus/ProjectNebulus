def encode_class(dictionary, class_name):
    """
    Encodes a class into a dictionary.
    """
    class_dict = {}
    for key, value in dictionary.items():
        if type(value) is list:
            class_dict[key] = []
            for item in value:
                if type(item) is dictionary:
                    class_dict[key].append(encode_class(item, class_name))
                else:
                    class_dict[key].append(item)
        elif type(value) is dictionary:
            class_dict[key] = encode_class(value, class_name)
        else:
            class_dict[key] = value
    class_dict['__class__'] = class_name
    return class_dict