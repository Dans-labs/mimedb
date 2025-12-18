import pkgutil
import importlib
from pathlib import Path

SOURCES_FOLDER = Path(__file__).parent / "sources"
DATA_FOLDER = "data/"
_types = {}
_reverse_types = {}
RUN_ONCE = False

def load_sources():
    """Dynamically load all sources from folder."""
    sources = {}
    package_name = "mimedb.sources"

    for finder, name, ispkg in pkgutil.iter_modules([str(SOURCES_FOLDER)]):
        module_name = f"{package_name}.{name}"
        module = importlib.import_module(module_name)
        if hasattr(module, "load") and callable(module.load):
            sources[name] = module
            module.load()
    return sources

def init():
    global RUN_ONCE
    if RUN_ONCE:
        return
    RUN_ONCE = True
    Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    global _types
    for source_name in sources.keys():
        module = sources[source_name]
        records = module.types()
        for r in records:
            extensions = _types.get(r["type"], [])
            extensions.extend(r["extensions"])
            extensions = list(set(extensions))
            _types[r["type"].lower()] = extensions

            for ext in r["extensions"]:
                type_tuple = (r["source"].lower(), r["type"].lower())
                types = _reverse_types.get(ext.lower(), [])
                types.append(type_tuple)
                types = list(set(types))
                _reverse_types[ext] = types

def get_types():
    return _types

def get_extensions():
    return _reverse_types

init()


    

