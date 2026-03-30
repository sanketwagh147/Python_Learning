# Builder Pattern — Question 3 (Hard)

## Problem: Deployment Pipeline Builder with Director

A DevOps team needs a configurable deployment pipeline. Different environments (dev, staging, production) have different pipeline configurations.

### Requirements

#### Part A: The Builder

Create `PipelineBuilder` that supports adding these stages:
- `add_lint(tool: str)` — e.g., "flake8", "pylint"
- `add_test(framework: str, coverage: bool)` — e.g., "pytest", with coverage flag
- `add_build(target: str)` — e.g., "docker", "wheel"
- `add_security_scan(scanner: str)` — e.g., "bandit", "snyk"
- `add_deploy(environment: str, strategy: str)` — e.g., ("production", "blue-green")
- `add_notify(channel: str)` — e.g., "slack", "email"
- `build()` returns a `Pipeline` dataclass with all configured stages.

#### Part B: The Director

Create `PipelineDirector` that uses the builder to create preset pipelines:

```python
class PipelineDirector:
    def __init__(self, builder: PipelineBuilder):
        self._builder = builder

    def build_dev_pipeline(self) -> Pipeline: ...
    def build_staging_pipeline(self) -> Pipeline: ...
    def build_production_pipeline(self) -> Pipeline: ...
```

**Dev pipeline**: lint + test (no coverage)  
**Staging pipeline**: lint + test (with coverage) + build + deploy("staging", "rolling")  
**Production pipeline**: lint + test (with coverage) + security scan + build + deploy("production", "blue-green") + notify("slack")

#### Part C: Custom Override

The Director should also support:
```python
director.build_production_pipeline(extra_notify="email")
# Same as production but ALSO notifies via email
```

### Expected Usage

```python
builder = PipelineBuilder()
director = PipelineDirector(builder)

dev = director.build_dev_pipeline()
print(dev)
# Pipeline(stages=['lint:flake8', 'test:pytest(coverage=False)'])

prod = director.build_production_pipeline(extra_notify="email")
print(prod)
# Pipeline(stages=['lint:flake8', 'test:pytest(coverage=True)', 'security:bandit',
#                   'build:docker', 'deploy:production(blue-green)',
#                   'notify:slack', 'notify:email'])
```

### Constraints

- Builder must be **reset** after each `build()` call.
- `Pipeline` should be a **dataclass** (or named tuple) — not just a dict.
- Use **ABC** for the builder interface so alternative builders (e.g., `YAMLPipelineBuilder`) could be swapped in.

### Think About

- How does the Director pattern differ from just having a factory method?
- What if stages have ordering constraints (e.g., security scan must come before deploy)?
- How would you serialize the `Pipeline` to a YAML config file?
