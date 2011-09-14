__author__ = 'dickon'


def configdriven():
    '''
    class decorator that uses the current class name to look up
    an actual class name to replace it.
    Allows a concrete or mock implementation to be substituted
    based on the content of the config module
    '''
    pass