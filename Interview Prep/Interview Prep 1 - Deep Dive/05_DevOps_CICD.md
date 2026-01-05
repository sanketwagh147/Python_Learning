# 05. DevOps, CI/CD & Cloud Infrastructure

## 🐳 1. Docker (Deep Dive)

### Layer Caching
Docker builds images in layers. Each instruction (`RUN`, `COPY`, `ADD`) creates a layer.
- **Mechanism:** If no lines change in `Dockerfile` and all context files (copied in) are identical, Docker reuses the cached layer.
- **Optimization:** Order matters! Put things that change often (source code) **after** things that change rarely (dependency installation).
```dockerfile
# BAD
COPY . .
RUN pip install -r requirements.txt

# GOOD (Utilizes cache for deps)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### Multi-Stage Builds
Reduces final image size by separating "Builder" environment from "Runtime" environment.
```dockerfile
# Stage 1: Build
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Run (Tiny Image)
FROM python:3.9-alpine
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["python", "app.py"]
```

### Docker Compose
Defines multi-container applications in a single YAML file.
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://db:5432/mydb
  db:
    image: postgres:14
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```
**Commands:** `docker-compose up -d`, `docker-compose down`, `docker-compose logs`.

### Container Networking
- **Bridge (Default):** Containers on same bridge can talk via container name.
- **Host:** Container shares host network. No port mapping needed.
- **None:** No networking. Isolated.
- **Overlay:** For multi-host networking (Docker Swarm/K8s).

### Volume Management
- **Named Volumes:** Managed by Docker. `docker volume create mydata`.
- **Bind Mounts:** Map host directory to container. `-v /host/path:/container/path`.
- **tmpfs:** Data stored in memory only (ephemeral).

---

## ☸️ 2. Kubernetes (K8s) (Deep Dive)

### Core Components
- **Control Plane:** API Server, Scheduler, Controller Manager, ETCD (key-value store).
- **Node Components:** Kubelet (runs containers), Kube-proxy (network rules), Container Runtime.

### Pods vs Deployments vs Services
- **Pod:** Smallest unit. One or more containers. Ephemeral (dies easily).
- **Deployment:** Manages Pods. Handles scaling (ReplicaSets) and updates (Rolling Updates).
- **Service:** Stable Network Endpoint for a set of Pods.
  - **ClusterIP:** Internal only.
  - **NodePort:** Expose on static port on each Node.
  - **LoadBalancer:** Provision cloud LB.

### Ingress
Routes external HTTP(S) traffic to Services.
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```
- **Ingress Controller:** Nginx, Traefik, AWS ALB Ingress Controller.

### Horizontal Pod Autoscaler (HPA)
Automatically scales Pods based on CPU/Memory.
```bash
kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=10
```

### Helm (The Package Manager)
- **Charts:** Templated K8s manifests.
- **Values.yaml:** Configuration file to inject varied settings into templates (e.g., `prod` vs `staging` configs).

---

## 🚀 3. CI/CD Pipeline Patterns (Deep Dive)

### Deployment Strategies
1. **Rolling Update (K8s Default):** Replace pods one by one. Zero downtime.
2. **Blue-Green Deployment:**
   - **Blue:** Current Prod.
   - **Green:** New Version.
   - **Switch:** Route traffic from Blue to Green instantly via LB.
   - **Pros:** Instant rollback. **Cons:** Costs double resources.
3. **Canary Release:**
   - Route 5% of traffic to New Version. Monitor errors. Gradually increase to 100%.

### Pipeline Stages (Example)
1. **Lint/Check:** `black`, `flake8`, type checking.
2. **Unit Test:** `pytest`.
3. **Build:** Docker build & Push to Registry (ECR/GCR).
4. **Deploy Staging:** `helm upgrade --install ...`
5. **Integration Test:** Run E2E tests against Staging.
6. **Deploy Prod:** Manual approval -> Canary Rollout.

### Secrets Management
**NEVER** commit secrets to Git.
- **K8s Secrets:** Base64 encoded (not secure enough alone).
- **External Secret Stores:** AWS Secrets Manager / HashiCorp Vault. Inject secrets into Pods as Environment Variables or Mounted Volumes at runtime.

### GitHub Actions (Example Workflow)
```yaml
name: CI Pipeline
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```
**Key Concepts:** `on` (triggers), `jobs` (parallel by default), `steps` (sequential), `uses` (reusable actions).

---

## 🏗️ 4. Infrastructure as Code: Terraform (Basics)

### Core Concept
Declarative config to provision cloud resources.
```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  tags = {
    Name = "MyWebServer"
  }
}
```
**Commands:**
- `terraform init`: Initialize providers.
- `terraform plan`: Preview changes.
- `terraform apply`: Execute changes.
- `terraform destroy`: Tear down infrastructure.

### State Management
Terraform stores state in `terraform.tfstate`.
- **Remote Backend (Best Practice):** Store state in S3 + DynamoDB for locking.

---

## ❓ Interview Questions & Answers

**Q1: Explain the difference between `COPY` and `ADD` in Dockerfile.**
> **A:** `COPY` simply copies local files. `ADD` can do that too, but also supports extracting TAR files automatically and downloading files from URLs (remote sources). Best practice: Use `COPY` unless you need the specific magic of `ADD`.

**Q2: What happens if a K8s Pod crashes?**
> **A:** The `kubelet` on the node restarts the container (based on `restartPolicy`). If the Pod is managed by a Deployment, and the Node dies, the Scheduler will reschedule the Pod to a healthy Node to maintain the desired replica count.

**Q3: How do you roll back a failed deployment?**
> **A:**
> - **K8s:** `kubectl rollout undo deployment/my-app`
> - **Helm:** `helm rollback my-release 1`
> - **CI/CD:** Revert the Git commit, which triggers the pipeline to deploy the previous trusted image.

**Q4: Container vs Virtual Machine?**
> **A:** VM virtualizes hardware (has its own OS kernel). Heavy. Container virtualizes the OS (shares the Host Kernel). Lightweight, fast startup.

---

## 🔗 Recommended Resources

- **Interactive:** [Play with Kubernetes](https://labs.play-with-k8s.com/)
- **Guide:** [The Twelve-Factor App (Methodology for SaaS)](https://12factor.net/)
- **CI/CD:** [GitLab CI/CD Pipelines Doc](https://docs.gitlab.com/ee/ci/pipelines/)
