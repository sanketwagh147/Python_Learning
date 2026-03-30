# Facade Pattern — Question 3 (Hard)

## Problem: Cloud Deployment Facade with Error Recovery

A deployment system wraps multiple cloud APIs. The facade must handle partial failures and rollback.

### Requirements

#### Subsystems
```python
class DNSProvider:
    def create_record(self, domain: str, ip: str) -> str: ...   # returns record_id
    def delete_record(self, record_id: str) -> None: ...

class ContainerRegistry:
    def push_image(self, image_tag: str) -> str: ...   # returns image_hash
    def delete_image(self, image_hash: str) -> None: ...

class KubernetesCluster:
    def create_deployment(self, image: str, replicas: int) -> str: ...   # returns deploy_id
    def delete_deployment(self, deploy_id: str) -> None: ...
    def wait_healthy(self, deploy_id: str, timeout: int) -> bool: ...

class SSLManager:
    def provision_cert(self, domain: str) -> str: ...   # returns cert_id
    def revoke_cert(self, cert_id: str) -> None: ...

class MonitoringService:
    def create_alerts(self, deploy_id: str) -> str: ...   # returns alert_group_id
    def delete_alerts(self, alert_group_id: str) -> None: ...
```

#### Facade
```python
class DeploymentFacade:
    def deploy(self, app_name: str, image_tag: str, domain: str, replicas: int = 3) -> DeploymentResult: ...
    def rollback(self, result: DeploymentResult) -> None: ...
```

`deploy()` orchestrates:
1. Push image → registry
2. Create K8s deployment → wait healthy
3. Provision SSL cert
4. Create DNS record
5. Set up monitoring alerts

**If ANY step fails, all previously completed steps must be rolled back in reverse order.**

### Expected Usage

```python
facade = DeploymentFacade(dns, registry, k8s, ssl, monitoring)

# Happy path
result = facade.deploy("myapp", "myapp:v2.1", "myapp.example.com", replicas=3)
# → Pushing myapp:v2.1... ✓
# → Creating deployment (3 replicas)... ✓
# → Waiting for healthy... ✓
# → Provisioning SSL for myapp.example.com... ✓
# → Creating DNS record... ✓
# → Setting up monitoring... ✓
# → Deployment complete!

# Failure at step 4 (SSL fails)
result = facade.deploy("myapp", "myapp:v2.2", "myapp.example.com")
# → Pushing myapp:v2.2... ✓
# → Creating deployment... ✓
# → Waiting for healthy... ✓
# → Provisioning SSL... ✗ (SSLError)
# → ROLLING BACK:
# →   Deleting deployment deploy-xyz... ✓
# →   Deleting image sha256:abc... ✓
# → DeploymentError: SSL provisioning failed. Rollback complete.
```

### Constraints

- Each step's result (IDs) must be tracked for rollback.
- Rollback must happen in **reverse order** of successful steps.
- The facade receives all subsystems via **constructor injection** (DIP).
- `DeploymentResult` is a dataclass tracking all created resource IDs.
- If rollback itself fails, log the error but continue rolling back remaining steps.

### Think About

- This is Facade + Saga. Where's the boundary between the two patterns?
- How would you make this idempotent (safe to retry)?
- In production, would you use a state machine or saga orchestrator instead of a facade?
