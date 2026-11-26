# pymjolnir

Design patterns for Python 3.13: a thread-safe registry, a singleton,
a multiton, and a chain of responsibility.

The package is not on PyPI. Install the wheel from the GitHub Release:

```bash
pip install "https://github.com/NjordLabs/pymjolnir/releases/download/v0.1.2/pymjolnir-0.1.2-py3-none-any.whl#sha256=26842daa3408884cf6bb70e3130f832ee8675426e957989c3e76d20bb31c8180"
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
