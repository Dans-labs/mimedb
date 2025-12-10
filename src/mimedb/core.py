import logging
import pkgutil

import importlib
from pathlib import Path

logger = logging.getLogger(__name__)


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
        # print(f"Importing module: {module_name}")
        module = importlib.import_module(module_name)
        if hasattr(module, "load") and callable(module.load):
            sources[name] = module
            module.load()
    return sources

def init():
    # print("Initializing TypeDB...")
    global RUN_ONCE
    if RUN_ONCE:
        return
    RUN_ONCE = True
    Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)
    # print("Loading sources...")
    # Automatically load adaptors on import
    sources = load_sources()
    # print(f"Loaded sources: {list(sources.keys())}")
    global _types
    for source_name in sources.keys():
        # print(f"Loading source: {source_name}")
        module = sources[source_name]
        records = module.types()
        # print(f"Records from {source_name}: {records}")
        for r in records:
            extensions = _types.get(r["type"], [])
            extensions.extend(r["extensions"])
            extensions = list(set(extensions))
            _types[r["type"]] = extensions

            for ext in r["extensions"]:
                type_tuple = (r["source"], r["type"])
                # full_mime_name = f"{module.MIME_PREFIX}{r['type']}" if hasattr(module, "MIME_PREFIX") else r["type"]
                types = _reverse_types.get(ext, [])
                # types.append(f"{r["source"]}:{r["type"]}")
                # types.append(full_mime_name)
                types.append(type_tuple)
                types = list(set(types))
                _reverse_types[ext] = types

def get_types():
    return _types

def get_extensions():
    return _reverse_types

init()


    

