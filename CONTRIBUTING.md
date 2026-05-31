# Contributing to lanyard.py

First off, thank you for considering contributing to `lanyard.py`! It's people like you who make the open-source community such an amazing place to learn, inspire, and create.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.12** or higher.
- **[uv](https://github.com/astral-sh/uv)** (highly recommended for dependency management).
- **Make** (optional, but recommended for using the provided automation).

## Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/nerma-now/lanyard.py.git
   cd lanyard.py
   ```

2. **Setup Development Environment**
   We use the `Makefile` to simplify the setup process. This will install all dependencies, extras, and setup `pre-commit` hooks.
   ```bash
   make dev
   ```

## Development Workflow

### 1. Branching
Always create a new branch for your changes:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 2. Code Quality
We maintain strict code quality standards using `ruff` and `mypy`. Before committing, ensure your code passes all checks.

- **Formatting and Linting**:
  ```bash
  make format
  ```
- **Type Checking**:
  ```bash
  make type
  ```

### 3. Testing
All new features or bug fixes should include tests. Run the test suite to ensure everything is working correctly:
```bash
make test
```

### 4. Running All Checks
To run all quality checks (formatting, typing, and tests) at once, use:
```bash
make all
```

## Pull Request Guidelines

1. **Keep it focused**: A single PR should address one bug fix or feature.
2. **Update Documentation**: If you're adding a new method or changing an existing one, please update the docstrings in the code.
3. **Follow the Style**: Ensure your code follows the Python 3.12+ standards used in this project (e.g., using new type alias syntax, generics, etc.).
4. **Be Descriptive**: Write a clear PR title and description explaining *what* changed and *why*.

## Code of Conduct
By participating in this project, you agree to abide by the terms of the [MIT License](LICENSE) and maintain a respectful environment for everyone.

---
*Happy coding!*
