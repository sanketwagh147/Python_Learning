# Adapter Pattern — Question 2 (Medium)

## Problem: Multi-Cloud Storage Adapter

Your app uses a unified storage interface, but you need to support AWS S3, Google Cloud Storage, and Azure Blob Storage — each has a completely different API.

### Requirements

- Your unified interface:
  ```python
  class CloudStorage(ABC):
      def upload(self, key: str, data: bytes) -> str: ...
      def download(self, key: str) -> bytes: ...
      def delete(self, key: str) -> bool: ...
      def list_files(self, prefix: str) -> list[str]: ...
  ```

- Third-party SDKs (simulate these — cannot modify):
  ```python
  class AWSS3Client:
      def put_object(self, bucket, key, body): ...
      def get_object(self, bucket, key) -> dict: ...
      def delete_object(self, bucket, key): ...
      def list_objects_v2(self, bucket, prefix) -> dict: ...

  class GCSClient:
      def upload_blob(self, bucket_name, blob_name, data): ...
      def download_blob(self, bucket_name, blob_name) -> bytes: ...
      def delete_blob(self, bucket_name, blob_name): ...
      def list_blobs(self, bucket_name, prefix) -> list: ...

  class AzureBlobClient:
      def upload_blob_data(self, container, blob, data): ...
      def download_blob_data(self, container, blob) -> bytes: ...
      def delete_blob_data(self, container, blob): ...
      def list_blobs_by_prefix(self, container, prefix) -> list: ...
  ```

- Create three adapters: `S3Adapter`, `GCSAdapter`, `AzureBlobAdapter`.

### Expected Usage

```python
def backup_data(storage: CloudStorage, key: str, data: bytes):
    """Works with ANY cloud provider — doesn't know which one."""
    storage.upload(key, data)
    files = storage.list_files("backups/")
    print(f"Backup complete. {len(files)} files in backups/")

# Swap provider with zero changes to business logic
backup_data(S3Adapter(AWSS3Client(), bucket="my-bucket"), "backups/db.sql", b"data")
backup_data(GCSAdapter(GCSClient(), bucket="my-bucket"), "backups/db.sql", b"data")
```

### Constraints

- Each adapter takes the raw SDK client + bucket/container name in constructor.
- Adapters must implement ALL 4 methods from `CloudStorage`.
- Business logic (`backup_data`) must depend only on the `CloudStorage` abstraction.

### Think About

- How does this follow the Dependency Inversion Principle?
- What if you need to add retry logic — where would it go? (Hint: Decorator on top of Adapter)
