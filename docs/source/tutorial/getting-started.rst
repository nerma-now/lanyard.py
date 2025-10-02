Getting Started
===============

Installation
------------

From github
~~~~~~~~~~~

pip
^^^^

.. code-block:: bash

    # Install core package
    pip install -U "lanyard.py @ git+https://github.com/nerma-now/lanyard.py"

    # Install with optional dependencies
    pip install -U "lanyard.py[dev] @ git+https://github.com/nerma-now/lanyard.py"
    pip install -U "lanyard.py[docs] @ git+https://github.com/nerma-now/lanyard.py"
    pip install -U "lanyard.py[test] @ git+https://github.com/nerma-now/lanyard.py"

    # Install all optional dependencies
    pip install -U "lanyard.py[dev,docs,test] @ git+https://github.com/nerma-now/lanyard.py"

uv
^^^^

.. code-block:: bash

    # Install core package
    uv add "lanyard.py @ git+https://github.com/nerma-now/lanyard.py"

    # Install with optional dependencies
    uv add "lanyard.py[dev] @ git+https://github.com/nerma-now/lanyard.py"
    uv add "lanyard.py[docs] @ git+https://github.com/nerma-now/lanyard.py"
    uv add "lanyard.py[test] @ git+https://github.com/nerma-now/lanyard.py"

    # Install all optional dependencies
    uv add "lanyard.py[dev,docs,test] @ git+https://github.com/nerma-now/lanyard.py"

From PyPI
~~~~~~~~~

pip
^^^^

.. code-block:: bash

    # Install core package
    pip install -U lanyard.py

    # Install with optional dependencies
    pip install -U "lanyard.py[dev]"
    pip install -U "lanyard.py[docs]"
    pip install -U "lanyard.py[test]"

    # Install all optional dependencies
    pip install -U "lanyard.py[dev,docs,test]"

uv
^^^^

.. code-block:: bash

    # Install core package
    uv add lanyard.py

    # Install with optional dependencies
    uv add "lanyard.py[dev]"
    uv add "lanyard.py[docs]"
    uv add "lanyard.py[test]"

    # Install all optional dependencies
    uv add "lanyard.py[dev,docs,test]"

Optional Dependencies Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The package provides the following optional dependency groups:

* **dev** - Development tools (black, mypy)
* **docs** - Documentation generation (sphinx)
* **test** - Testing framework (pytest, pytest-asyncio)

You can combine multiple groups by separating them with commas, for example ``[dev,test]``.

Example
-------

Here's a basic example of how to use lanyard.py:

.. literalinclude:: ../../../example/basic_usage.py
    :language: python
    :linenos: