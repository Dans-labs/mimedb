# mimedb

Convert between file extensions and mimetypes and vice-versa

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
```
