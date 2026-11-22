# pymjolnir

Design patterns for Python: a thread-safe registry, singleton, multiton, and chain of responsibility.

```bash
pip install pymjolnir
```

Pin a release tag. The package requires Python 3.13.

```python
from pymjolnir import Registry, singleton

registry = Registry()
registry.register("echo", lambda value: value)
registry.create("echo", "ok")
```

Source and issues: https://github.com/NjordLabs/pymjolnir
