# fabric-logging

Logging utility for Microsoft Fabric notebooks.

## Usage

```python
# import statement & setup
from fabric_logging import build_logger
log = build_logger(name="notebook_name", level=2)

# emit log
log.info("Starting ingestion")
```