# Architecture Design Document — Smission Core Engine

## 1. System Architecture
Smission uses a modular, layered architecture designed for separation of concerns and database independence:

```
┌────────────────────────────────────────────────────────┐
│                      Presentation Layer (API)          │
│          App Routes, Controller Routers, JSON DTOs     │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                        Service Layer                   │
│          Business Rules, Orchestration, Engines        │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│                      Data Access Layer                 │
│         SQLAlchemy Models, Base Class, DB Sessions     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Key Architectural Patterns

### 2.1. Domain-Driven Service Layout
Business logic is isolated into dedicated, cohesive service files in `app/services`:
- `auth_service.py`: Authentication, registration, and user profiles.
- `assessment_service.py`: Session transitions and submission orchestration.
- `assessment_engine.py`: Dynamic question evaluation using the **Strategy Pattern**.

### 2.2. Event Outbox Pattern
To prevent dual-write vulnerabilities (where a database write succeeds but an event publication fails):
1. Any operation that changes state (e.g. `USER_REGISTERED`, `ASSESSMENT_COMPLETED`) writes the event to the `event_outbox` table in the same local transaction.
2. A separate background worker polls the `event_outbox` table, delivers the events to external systems (or Redis/PubSub), and marks them as processed.

### 2.3. Audit Logging Middleware & Mixin
- To ensure enterprise-level compliance, crucial operations write structured records to the `audit_logs` table.
- Log payloads capture:
  - Who executed the change (`created_by`, `updated_by`).
  - IP Address and User-Agent.
  - Snapshot of modified entity fields.

---

## 3. Database Layer Architecture
- **ORM**: SQLAlchemy 2.0 with type annotations and relationship lazy-loading optimizations.
- **Migrations**: Alembic handles versioned schema upgrades/downgrades.
- **Transaction Isolation**: Lock levels are handled explicitly (e.g., `with_for_update()`) for concurrent transactions (like registration running counters).
