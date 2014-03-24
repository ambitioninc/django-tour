def import_string(module_string):
    path = '.'.join(module_string.split('.')[:-1])
    module_name = module_string.split('.')[-1]
    file_name = module_string.split('.')[-2]

    try:
        module_path = __import__(path, globals(), locals(), [file_name])
    except ImportError:
        return None

    if not module_path or not hasattr(module_path, module_name):
        return None

    module = getattr(module_path, module_name)
    if not module:
        return None

    return module
