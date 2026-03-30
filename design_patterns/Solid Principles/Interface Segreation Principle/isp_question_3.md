# Interface Segregation Principle — Question 3 (Hard)

## Problem: Refactor a Cloud Service SDK with Fat Interfaces

A cloud provider SDK has a single `CloudService` interface with 15+ methods. Different service types only use a subset. Refactor using ISP and write a type-safe client.

### The Violating Code

```python
class CloudService(ABC):
    # Compute
    @abstractmethod
    def create_instance(self, config): ...
    @abstractmethod
    def stop_instance(self, id): ...
    @abstractmethod
    def start_instance(self, id): ...
    @abstractmethod
    def terminate_instance(self, id): ...
    
    # Storage
    @abstractmethod
    def upload_file(self, bucket, key, data): ...
    @abstractmethod
    def download_file(self, bucket, key): ...
    @abstractmethod
    def delete_file(self, bucket, key): ...
    @abstractmethod
    def list_files(self, bucket): ...
    
    # Database
    @abstractmethod
    def create_table(self, name, schema): ...
    @abstractmethod
    def query(self, table, conditions): ...
    @abstractmethod
    def insert(self, table, data): ...
    
    # Messaging
    @abstractmethod
    def publish(self, topic, message): ...
    @abstractmethod
    def subscribe(self, topic, callback): ...
    
    # Monitoring
    @abstractmethod
    def get_metrics(self, resource_id): ...
    @abstractmethod
    def set_alarm(self, metric, threshold, callback): ...
```

### Task

#### 1. Split into focused interfaces
```python
class ComputeService(ABC): ...     # create, stop, start, terminate instances
class StorageService(ABC): ...     # upload, download, delete, list files
class DatabaseService(ABC): ...    # create_table, query, insert
class MessagingService(ABC): ...   # publish, subscribe
class MonitoringService(ABC): ...  # get_metrics, set_alarm
```

#### 2. Concrete implementations
- `AWSCompute(ComputeService)`: EC2-like
- `AWSStorage(StorageService)`: S3-like
- `AWSDatabase(DatabaseService)`: DynamoDB-like
- `MinimalProvider(ComputeService, StorageService)`: budget provider with only compute + storage

#### 3. Type-safe clients that declare their dependencies
```python
class DeploymentManager:
    """Needs compute + storage only."""
    def __init__(self, compute: ComputeService, storage: StorageService): ...

class DataPipeline:
    """Needs storage + database + messaging."""
    def __init__(self, storage: StorageService, db: DatabaseService, messaging: MessagingService): ...

class FullStackApp:
    """Needs everything."""
    def __init__(self, compute: ComputeService, storage: StorageService,
                 db: DatabaseService, messaging: MessagingService, monitoring: MonitoringService): ...
```

### Expected Usage

```python
# AWS full suite
aws_compute = AWSCompute(region="us-east-1")
aws_storage = AWSStorage(region="us-east-1")
aws_db = AWSDatabase(region="us-east-1")

deploy = DeploymentManager(compute=aws_compute, storage=aws_storage)
deploy.deploy_app("my-app")  # Only uses compute + storage

# Budget provider — only has compute + storage
budget = MinimalProvider(api_key="...")
deploy2 = DeploymentManager(compute=budget, storage=budget)  # Works!

# Can't use budget provider for data pipeline — no DB or messaging
# pipeline = DataPipeline(storage=budget, db=budget, messaging=budget)  # Type error!
```

### Constraints

- Each interface has 2-5 methods max.
- No class implements methods it doesn't support.
- Clients declare ONLY the interfaces they need (not the full `CloudService`).
- Adding a new service type (e.g., `CDNService`) is a new interface — existing code untouched.
- Use `typing.Protocol` for at least one interface to demonstrate structural subtyping.

### Think About

- How does AWS SDK actually organize its services? (Each service is a separate client.)
- What's the relationship between ISP and the Facade pattern?
- How do protocols enable ISP without inheritance?
- At what point do too many interfaces become a burden? How do you find the right granularity?
