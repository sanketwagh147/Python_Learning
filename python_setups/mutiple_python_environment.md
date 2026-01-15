# Software Engineering Guide: Managing Multiple Python Versions

Managing Python versions effectively is critical for maintaining stable development environments across different projects. This guide outlines the implementation of **pyenv**, the industry-standard tool for version management.

## 1. Context & Rationale
For professional software engineering, relying on the system Python (the one pre-installed by your OS) is a major anti-pattern. Upgrading system Python can break OS utilities, and different projects often require conflicting versions (e.g., a legacy app on 3.8 vs. a new microservice on 3.12).

### Guiding Principles
- **Isolation**: Each project should define its own version.
- **Reproducibility**: Use `.python-version` files to ensure all teammates use the exact same runtime.
- **Minimalism**: Use shims to intercept commands rather than hardcoding aliases.

---

## 2. Recommended Solution: `pyenv`



### Phase A: Install Build Dependencies
Python is compiled from source to ensure it is optimized for your specific hardware.

**macOS:**
```bash
brew install openssl readline sqlite3 xz zlib tcl-tk
```

**Ubuntu/Debian:**

```bash
sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

### Phase B: Install pyenv

```bash
curl https://pyenv.run | bash
```

### Phase C: Shell Configuration

Add the following to your profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Pyenv Configuration
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

**Reload your shell:**
```bash
source ~/.zshrc  # For zsh
# OR
source ~/.bashrc  # For bash
```

> **Note:** You may need to restart your terminal completely for changes to take effect.

---

## 3. Implementation Workflow

### Installing New Versions

```bash
# View all available versions (including Dev and RC)
pyenv install --list | grep " 3.1"

# Install specific stable versions
pyenv install 3.11.9
pyenv install 3.12.3

# Verify installed versions
pyenv versions
```

### Switching Contexts

```bash
# Global: Default for your user account
pyenv global 3.12.3

# Local: Automatically switches when you enter this directory
# This creates a .python-version file
pyenv local 3.11.9

# Shell: Only for the current shell session
pyenv shell 3.10.8

# Check which Python version is currently active
pyenv version

# Check which Python executable is being used
which python
python --version
```

---

## 4. Comparison of Modern Tools

| Tool | Recommended Use Case | Strategy |
|------|---------------------|----------|
| **pyenv** | Standard Web/Backend Dev | Shims & Source Compilation |
| **uv** | High-performance / Modern CI | Rust-based binary management |
| **Conda** | Data Science / ML | Pre-compiled binaries + Env mgmt |
| **asdf** | Polyglot (Node + Python + Go) | Universal plugin system |

---

## 5. Trade-offs & Scaling

* **Compilation Time**: Compiling Python from source can take 2–5 minutes depending on CPU.
* **Binary Compatibility**: Ensure `openssl` is correctly linked on macOS (Homebrew usually handles this, but it’s a common failure mode).
* **Automation**: In a CI/CD pipeline, prefer pre-built Docker images over `pyenv` to reduce build times.

---

## 6. Common Troubleshooting

### Issue: `pyenv: command not found`
**Solution:** Ensure the shell configuration is correct and reload your shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### Issue: Python compilation fails on macOS
**Solution:** Install Xcode Command Line Tools and verify Homebrew packages:
```bash
xcode-select --install
brew update && brew upgrade
```

### Issue: Wrong Python version is being used
**Solution:** Check the priority order (shell > local > global):
```bash
pyenv version
pyenv versions
cat .python-version  # Check if local version file exists
```

---

## 7. Next Steps

* **Project Scaffolding**: Integrate `pyenv` with **Poetry** or **uv** for robust dependency management.
* **Workflow Optimization**: Create scripts to automate the installation of your standard toolset (linters, formatters) across every new Python version.
* **Virtual Environments**: Use `pyenv-virtualenv` plugin for creating isolated environments per project.

### Example: Creating a Virtual Environment with pyenv

```bash
# Install pyenv-virtualenv plugin (if not already installed)
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv

# Create a virtual environment
pyenv virtualenv 3.12.3 myproject-env

# Activate it
pyenv activate myproject-env

# Set it as the local environment for a project
pyenv local myproject-env

# Deactivate
pyenv deactivate
```

---

## 8. Additional Resources

- [pyenv GitHub Repository](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv Plugin](https://github.com/pyenv/pyenv-virtualenv)
- [Python Official Downloads](https://www.python.org/downloads/)
- [uv - Fast Python Package Installer](https://github.com/astral-sh/uv)

---

**Note:** For high-performance modern CI/CD pipelines, consider exploring **uv**, which is currently the fastest way to manage both Python versions and project dependencies in a single Rust-based tool.