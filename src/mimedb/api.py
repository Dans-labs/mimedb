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

def related_extensions(extension):
    '''Returns the list of related extensions for a given extension.'''

    types = get_types(extension)
    equivalent = set()
    for s,t in types:
        extensions = get_extensions(t)
        for e in extensions:
            if e.lower() != extension.lower():
                equivalent.add(e)
    return list(equivalent)

def equivalent_types(type):
    '''Returns the list of equivalent types for a given type.'''

    extensions = get_extensions(type)
    equivalent = set()
    for ext in extensions:
        types = get_types(ext)
        for s,t in types:
            if t.lower() != type.lower():
                equivalent.add(t)
    return list(equivalent)
