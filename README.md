# pymjolnir

Design patterns for Python 3.13: a thread-safe registry, a singleton,
a multiton, and a chain of responsibility.

The package is not on PyPI. When `v0.1.0` is published, install that
tag:

```bash
pip install "pymjolnir @ git+https://github.com/NjordLabs/pymjolnir.git@v0.1.0"
```

```python
from pymjolnir import Registry

registry = Registry()
registry.register("echo", lambda value: value)
registry.create("echo", "ok")
```

`singleton` and `multiton` cache one instance, or one instance per
key. `Chain` runs handlers in order until one returns a value.

Source and issues: [NjordLabs/pymjolnir](https://github.com/NjordLabs/pymjolnir)
