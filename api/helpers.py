def dictify(item):
    return item.__dict__

def dictify_all(listed):
    new_list = []
    for item in listed:
        new_list.append(dictify(item))
    return new_list
