# UV Quick Reference Guide

## What is UV?

**UV** is an extremely fast Python package and project manager written in Rust. It replaces pip, pip-tools, Poetry, and virtualenv:

- 🚀 **10-100x faster** than pip
- 🔒 **Lockfiles** for reproducible builds
- 🎯 **Virtual environments** auto-managed
- 📦 **Project management** (PEP 621 compliant)
- ⚡ **Zero configuration** required

Developed by Astral (creators of Ruff).

## Typical Project Structure

```
my-project/
├── pyproject.toml          # Project config & dependencies
├── uv.lock                 # Locked versions (auto-generated)
├── .venv/                  # Virtual environment (auto-managed)
├── .python-version         # Python version lock
└── src/
    └── __init__.py
```

---

## Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Homebrew
brew install uv

# pip (not recommended)
pip install uv

# Verify
uv --version
```

---

## Quick Start

```bash
# Create new project
uv init my-project
cd my-project

# Or initialize in existing directory
uv init

# Install dependencies
uv sync

# Add packages
uv add requests pandas
uv add --dev pytest ruff

# Run scripts
uv run python main.py
uv run pytest
```

---

## Essential Commands

### Project Initialization

```bash
uv init                    # Initialize new project
uv init --python 3.12      # With specific Python version
```

### Dependency Management

```bash
# Add packages
uv add <package>           # Add runtime dependency
uv add --dev <package>     # Add dev dependency
uv add "package[extra]"    # Add with extras

# Remove packages
uv remove <package>
uv remove --dev <package>

# Sync environment
uv sync                    # Install all dependencies
uv sync --extra dev        # Include optional group
uv sync --all-extras       # Include all optional groups
```

### Running Code

```bash
uv run python script.py    # Run Python script
uv run python -m module    # Run module
uv run pytest              # Run commands from venv
```

### Lock & Update

```bash
uv lock                    # Update lockfile
uv lock --upgrade          # Update all to latest versions
uv sync                    # Sync venv with lockfile
```

### Virtual Environments

```bash
uv venv                    # Create .venv (auto-done by uv sync)
uv venv --python 3.11      # With specific Python
source .venv/bin/activate  # Manual activation (optional)
```

---

## pyproject.toml Template

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "you@example.com" }
]

dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Common Workflows

### Starting a New Project
```bash
uv init my-project && cd my-project
uv add requests pytest --dev
uv sync
uv run python main.py
```

### Adding to Existing Project
```bash
uv init                    # Creates pyproject.toml
uv add $(cat requirements.txt)  # Migrate from requirements.txt
uv sync
```

### Daily Development
```bash
uv add <package>           # Add new dependency
uv sync                    # Sync environment
uv run pytest              # Run tests
uv lock --upgrade          # Update dependencies weekly
```

---

## UV vs Other Tools

| Feature | UV | pip | Poetry | PDM |
|---------|:--:|:---:|:------:|:---:|
| **Speed** | ⚡⚡⚡ | ⚡ | ⚡⚡ | ⚡⚡ |
| **Lockfile** | ✅ | ❌ | ✅ | ✅ |
| **Auto venv** | ✅ | ❌ | ✅ | ✅ |
| **Setup** | Easy | Easy | Medium | Medium |
| **PEP 621** | ✅ | ✅ | ✅ | ✅ |

---

## Best Practices

✅ **Commit:** `pyproject.toml`, `uv.lock`, `.python-version`  
❌ **Don't commit:** `.venv/`, `__pycache__/`

```bash
# .gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

**Tips:**
- Use `uv sync` to ensure consistent environments across team
- Run `uv lock --upgrade` monthly to update dependencies
- Pin Python version in `.python-version` file
- Use optional dependencies for different environments/features

---

## Troubleshooting

### Command not found
```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.zshrc
```

### Wrong Python version
```bash
echo "3.11" > .python-version
uv venv --python 3.11
```

### Dependency conflicts
```bash
uv lock --upgrade
uv cache clean
```

### Slow installation
```bash
uv cache clean           # Clear cache
uv sync --reinstall      # Fresh install
```

---

## Cheat Sheet

```bash
# Setup
uv init                  # Initialize project
uv sync                  # Install dependencies

# Add/Remove
uv add <pkg>             # Add dependency
uv add --dev <pkg>       # Add dev dependency
uv remove <pkg>          # Remove dependency

# Run
uv run <cmd>             # Run command in venv
uv run python script.py  # Run Python script

# Update
uv lock --upgrade        # Update all dependencies
uv add <pkg> --upgrade   # Update specific package

# Info
uv --version             # UV version
uv pip list              # List installed packages
```

---

## Additional Resources

- [UV GitHub](https://github.com/astral-sh/uv)
- [UV Documentation](https://docs.astral.sh/uv/)
- [PEP 621 Specification](https://peps.python.org/pep-0621/)
- [Ruff Linter](https://github.com/astral-sh/ruff)
