def dictify(item):
    return item.__dict__

def dictify_all(listed):
    new_list = []
    for item in listed:
        new_list.append(dictify(item))
    return new_list

# def validate_search_query(q):
#     if len(q) < 2:
#         return Exception()
