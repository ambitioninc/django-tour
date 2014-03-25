def import_string(module_string):
    parts = module_string.split('.')
    assert len(parts) > 1

    path = '.'.join(parts[:-1])
    module_name = parts[-1]
    file_name = parts[-2]
    print path, module_name, file_name

    try:
        print 'try it'
        module_path = __import__(path, globals(), locals(), [file_name])
        print 'path', module_path
    except ImportError:
        return None

    if not module_path or not hasattr(module_path, module_name):
        return None

    module = getattr(module_path, module_name)
    if not module:
        return None

    return module
