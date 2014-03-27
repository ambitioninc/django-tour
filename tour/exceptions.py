
class MissingStepClass(Exception):
    """
    This exception is meant to be raised when a step is being created but it does not
    have a class defined
    """
    pass


class MissingTourClass(Exception):
    """
    This exception is meant to be raised when a tour is being created but it does not
    have a class defined
    """
    pass
