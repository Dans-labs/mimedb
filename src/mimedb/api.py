import mimedb.core as core

def types2extensions():
    '''Returns the mapping of types to extensions.'''

    return core.get_types()

def extensions2types():
    '''Returns the mapping of extensions to types.'''

    return core.get_extensions()

def get_types(extension):
    '''Returns the list of types for a given extension.'''

    db = core.get_extensions()
    return db.get(extension.lower(), [])

def get_extensions(type):
    '''Returns the list of extensions for a given type.'''

    db = core.get_types()
    return db.get(type.lower(), [])
