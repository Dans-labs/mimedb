# mimedb

Convert between file extensions and mimetypes and vice-versa. Uses source files from mime-db (https://github.com/jshttp/mime-db) and galaxy-datatypes (https://github.com/galaxyproject/galaxy).

## Installation

```bash
uv add https://github.com/Dans-labs/mimedb.git
```

## Usage

```python
import mimedb
# Get mimetype from file extension
#[('galaxy', 'galaxy.datatypes.sequence:Fasta')]
(source, mime_type) = mimedb.get_types("fasta")
# Get file extension from mimetype
# ["json", ...]
json_file_extensions = mimedb.get_extensions("application/json")
# Get equivalent types
# ['galaxy.datatypes.text:json', ...]
json_equivalents = mimedb.equivalent_types("application/json")

```
