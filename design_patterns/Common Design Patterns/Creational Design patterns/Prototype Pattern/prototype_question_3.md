# Prototype Pattern — Question 3 (Hard)

## Problem: Cloud Infrastructure Template System

A cloud platform allows users to clone pre-configured infrastructure templates (like AWS CloudFormation).

### Requirements

#### Resources

```python
class Resource(ABC):
    name: str
    region: str
    tags: dict[str, str]

    @abstractmethod
    def clone(self) -> Resource: ...
    
    @abstractmethod
    def estimate_cost(self) -> float: ...
```

Concrete resources:
- `VM(Resource)`: cpu_cores, ram_gb, os_image, storage_gb
- `Database(Resource)`: engine (postgres/mysql), storage_gb, replicas
- `LoadBalancer(Resource)`: algorithm (round-robin/least-connections), target_vms: list[VM]

#### InfraTemplate

```python
class InfraTemplate:
    """A named collection of resources that can be cloned as a unit."""
    name: str
    resources: list[Resource]
    
    def clone(self, new_name: str) -> InfraTemplate: ...
    def total_cost(self) -> float: ...
    def add_resource(self, resource: Resource): ...
```

#### Pre-built Templates

- **"web-starter"**: 1 VM (2 cpu, 4gb ram, ubuntu, 50gb) + 1 Database (postgres, 20gb, 0 replicas)
- **"production-ha"**: 3 VMs + 1 Database (postgres, 100gb, 2 replicas) + 1 LoadBalancer pointing to VMs

### Expected Usage

```python
# Clone and customize
my_infra = registry.clone_template("production-ha", "my-app-prod")
my_infra.resources[0].ram_gb = 16  # upgrade first VM
my_infra.resources[3].algorithm = "least-connections"

# Original template is UNCHANGED
original = registry.get_template("production-ha")
assert original.resources[0].ram_gb == 4  # still 4gb

# Cost estimation
print(my_infra.total_cost())  # sum of all resource costs
```

### Key Challenge — Circular References

The `LoadBalancer` holds references to `VM` objects. When cloning the template:
- The cloned LoadBalancer must point to the **cloned VMs**, NOT the original VMs.
- Modifying a cloned VM's config should reflect in the cloned LoadBalancer's target list.

### Constraints

- Handle the circular reference problem (LoadBalancer → VMs) correctly.
- Implement `__copy__` and `__deepcopy__` on `InfraTemplate` to handle this.
- Write a test that proves modifying a cloned VM's RAM does NOT affect the original template.

### Think About

- How does `copy.deepcopy` handle object graphs with shared references?
- What's the `memo` parameter in `__deepcopy__`? Why does it matter here?
- Could you combine Prototype + Registry + Builder patterns here?
