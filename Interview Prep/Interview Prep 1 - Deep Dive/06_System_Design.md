# 06. System Design & Scalability Patterns

## 🏛️ 1. Core Architecture Concepts

### Scalability (Vertical vs Horizontal)
- **Vertical (Scale Up):** Buy a bigger server (more RAM, more CPU). Easier but has a hardware limit.
- **Horizontal (Scale Out):** Add more servers. Harder (requires load balancing, statelessness) but theoretically infinite.

### CAP Theorem
In a distributed data store, you can only pick 2 out of 3:
1. **Consistency:** All nodes see the same data at the same time.
2. **Availability:** Every request gets a (non-error) response.
3. **Partition Tolerance:** System continues to work despite message loss/network failure between nodes.
> In reality, Partition Tolerance (P) is unavoidable in distributed systems. You choose between **CP** (Consistency > Availability, e.g., Banking - fail if unsure) and **AP** (Availability > Consistency, e.g., Social Feed - show slightly old data).

### Load Balancing
- **L4 (Transport Layer):** Routes based on IP + Port (e.g., TCP connection). Very fast.
- **L7 (Application Layer):** Routes based on HTTP Header, URL path, etc. (e.g., Nginx, AWS ALB).

---

## ☁️ 2. AWS Cloud Services (Deep Dive)

### Compute
- **EC2:** Virtual Machines. You manage OS.
- **Lambda:** Serverless. Event-driven code. Cold starts can be an issue.
- **ECS/EKS:** Container Orchestration (Docker/K8s).

### Storage
- **S3 (Simple Storage Service):** Object storage (images, logs, backups). Infinite scale. 99.999999999% durability.
- **EBS (Elastic Block Store):** Hard drive attached to EC2. Fast, low latency.

### Databases
- **RDS:** Managed Relational DB (Postgres, MySQL). Handles backups/patching.
- **DynamoDB:** Managed NoSQL (Key-Value). Single-digit millisecond latency at any scale.

### Messaging (Decoupling)
- **SQS (Simple Queue Service):** Pull-based. Producer -> Queue -> Consumer polls.
- **SNS (Simple Notification Service):** Push-based. Pub/Sub. Publisher -> Topic -> Multiple Subscribers (Email, Lambda, SQS).

---

## 📐 3. Common Design Questions (Deep Dive)

### Design a Rate Limiter
**Goal:** Prevent abuse. Limit user to X req/sec.
- **Algorithms:**
  - **Token Bucket:** Add tokens at rate `r`. Request eats a token. If bucket empty -> 429. Burst friendly.
  - **Leaky Bucket:** Requests enter queue. Processed at constant rate. Smooths traffic.
  - **Fixed Window Counter:** Reset counter every minute. Edge case: Spike at minute boundary 00:59 and 01:00 allows double limit.
- **Storage:** Redis (Atomic counters + Expiry).

### Design a URL Shortener (TinyURL)
**Goal:** Map `long_url` <-> `short_code` (e.g., `ax7B`).
1. **Hashing:** `MD5(long_url)`. Taking first 7 chars? Collision risk.
2. **Encoding ID:** Use Auto-Increment DB ID (1000001). Convert Base10 to Base62 (a-z, A-Z, 0-9).
   - ID `125` -> `cb`. Short URL: `site.com/cb`.
   - **Scale:** High Read/Write ratio. Cache hot redirections in Redis.

### Caching Strategies
- **Cache-Aside (Lazy Loading):** App checks Cache. Miss? Read DB -> Write to Cache -> Return. 
  - *Risk:* Stale data if DB updates but cache doesn't.
- **Write-Through:** App writes to Cache AND DB strictly.
  - *Pros:* Consistency. *Cons:* Slow writes.

---

## 🏗️ 4. Microservices Architecture (Deep Dive)

### When to Use
- **Monolith First:** Start simple. Split when team/codebase grows.
- **Signs to Split:** Independent scaling needs, separate deployment cycles, team ownership boundaries.

### Patterns
- **API Gateway:** Single entry point. Routes to services. Handles auth, rate limiting.
- **Service Discovery:** Services register themselves. Clients query registry (e.g., Consul, AWS Service Discovery).
- **Circuit Breaker:** Prevents cascade failures. If Service B fails, stop calling it temporarily.

### Challenges
- **Distributed Tracing:** Use correlation IDs. Tools: Jaeger, Zipkin.
- **Data Consistency:** Saga pattern for distributed transactions.

---

## 🗺️ 5. More AWS Deep Dives

### API Gateway
Managed service to create, publish, and manage APIs.
- Routes requests to Lambda, EC2, or any HTTP endpoint.
- Handles throttling, caching, authorization.

### IAM (Identity and Access Management)
- **Users:** Humans.
- **Roles:** Assigned to services/resources (e.g., EC2 can assume a role to access S3).
- **Policies:** JSON documents defining permissions (Allow/Deny actions on resources).
- **Principle of Least Privilege:** Grant only necessary permissions.

### VPC (Virtual Private Cloud)
Your isolated network in AWS.
- **Subnets:** Public (internet-facing) vs Private (internal only).
- **Security Groups:** Stateful firewall at instance level.
- **NACLs:** Stateless firewall at subnet level.

### CloudWatch
Monitoring and observability.
- **Metrics:** CPU, Memory, Custom metrics.
- **Logs:** Centralized log collection.
- **Alarms:** Trigger actions (e.g., SNS notification, Auto Scaling).

---

## 📐 6. Additional Design Questions

### Design a Deployment Pipeline (Critical for this Role!)
**Goal:** Automate code -> production with confidence.
1. **Source:** Git push triggers pipeline.
2. **Build:** Lint, Test, Docker Build.
3. **Staging Deploy:** Helm install to staging K8s.
4. **E2E Tests:** Selenium/Playwright against staging.
5. **Prod Deploy:** Manual approval -> Canary rollout.
6. **Monitoring:** CloudWatch alerts, rollback trigger.

### Design a Notification System
**Goal:** Send push/email/SMS to millions of users.
- **Components:** API -> Message Queue (SQS/Kafka) -> Workers -> Delivery Services (SNS, Twilio).
- **Fanout:** Use SNS topic to fanout to SQS queues per notification type.
- **User Preferences:** Store in DB. Filter at worker level.
- **Rate Limiting:** Prevent spamming users.

### Database Sharding
**Goal:** Horizontal partitioning of data across multiple DBs.
- **Shard Key:** Choose wisely (e.g., `user_id`). Determines which shard holds data.
- **Consistent Hashing:** Minimizes data movement when shards added/removed.
- **Trade-off:** Cross-shard queries are expensive. Design to minimize them.

---

## ❓ Interview Questions & Answers

**Q1: How do you handle "Hot Partitions" in a database?**
> **A:** This happens if one shard receives disproportionate traffic (e.g., Justin Bieber's tweets). 
> - **Solution:** Consistent Hashing with Virtual Nodes to balance load. For read-hot keys, use aggressive Caching (Redis).

**Q2: Explanation of Consistent Hashing?**
> **A:** Maps both Nodes and Keys to a circle (0-360 deg). Key is stored in the next closest Node clockwise. When a Node is added/removed, only Keys in its immediate neighbor segment need remapping, not the whole DB.

**Q3: Best practice for handling DB Failover?**
> **A:** Use Primary-Replica setup. Writes go to Primary. Reads to Replicas. If Primary dies, promote a Replica to Primary automatically (e.g., using AWS RDS Multi-AZ).

---

## 🔗 Recommended Resources

- **Bible:** [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer)
- **Book:** "Designing Data-Intensive Applications" by Martin Kleppmann (Must read chapters: Replication, Partitioning).
- **Video:** [High Scalability - Real life architectures](http://highscalability.com/)
