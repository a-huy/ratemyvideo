def capitalize_name(in_name):
    parts = in_name.strip().split(' ')
    return ' '.join([x[0].upper() + x[1:] for x in parts])
