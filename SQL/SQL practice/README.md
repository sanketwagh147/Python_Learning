# SQL Practice - PostgreSQL

## Connection
```
postgresql://sanket@localhost:5432/local_db
```

## Setup
Run these files in order:
```bash
psql "postgresql://sanket@localhost:5432/local_db" -f "00_schema_setup.sql"
psql "postgresql://sanket@localhost:5432/local_db" -f "01_dummy_data.sql"
```

## Database Schema (E-Commerce Company)

```
departments ──────< employees ──────< salary_history
                       │
                       ├──────< employee_projects >──────── projects
                       │
categories ──────< products ──────< order_items >──────── orders ──────> customers
    │                  │                                                     │
    └─ (self-ref)      ├──────< reviews <─────────────────────────────────────┘
                       ├──────< inventory                   shipping_addresses
                       └──────> suppliers
```

### Table Row Counts
| Table | Rows | Description |
|-------|------|-------------|
| departments | 10 | Company departments |
| employees | 32 | Active & inactive employees with hierarchy |
| salary_history | 17 | Historical salary changes |
| projects | 13 | Company projects with status |
| employee_projects | 30 | Many-to-many assignment |
| categories | 16 | Product categories (hierarchical) |
| suppliers | 10 | Product suppliers |
| products | 40 | Product catalog |
| customers | 25 | Registered customers |
| shipping_addresses | 10 | Customer shipping addresses |
| orders | 41 | Orders (various statuses) |
| order_items | 78 | Individual items in orders |
| reviews | 39 | Product reviews with ratings |
| inventory | 38 | Inventory change log |

## Practice Files

| File | Focus | Questions |
|------|-------|-----------|
| `02_DQL_select_queries.sql` | SELECT, JOINs, Subqueries, Window Functions, CTEs, Aggregation, Set Operations | ~45 problems |
| `03_DML_manipulation.sql` | INSERT, UPDATE, DELETE, UPSERT, Transactions | ~15 problems |
| `04_DDL_definitions.sql` | CREATE TABLE, ALTER, Views, Indexes, Triggers, Partitioning | ~12 problems |
| `05_optimization.sql` | EXPLAIN ANALYZE, Index strategy, Anti-patterns, Query rewriting | ~15 problems |
| `06_advanced_interview.sql` | FAANG-level: Gaps & Islands, Cohort Analysis, Market Basket, Fraud Detection | 8 deep problems |

## Difficulty Legend
- 🟢 Easy - Basic SQL, single concept
- 🟡 Medium - Multiple concepts, real-world scenarios  
- 🔴 Hard - Multi-step, requires deep understanding
- 🔴🔴 Interview Level - Commonly asked in tech interviews

## How to Practice
1. Read the problem statement carefully
2. Write a SELECT to explore relevant tables first
3. Build your solution incrementally (CTE by CTE)
4. Use `EXPLAIN (ANALYZE, BUFFERS)` to check performance
5. Compare your approach with the hints only if stuck

## Reset Database
If you mess up the data while practicing DML:
```bash
psql "postgresql://sanket@localhost:5432/local_db" -f "00_schema_setup.sql"
psql "postgresql://sanket@localhost:5432/local_db" -f "01_dummy_data.sql"
```
