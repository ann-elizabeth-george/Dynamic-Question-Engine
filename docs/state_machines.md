# State Machines — Smission Core Engine

This document details the state lifecycles for critical components of the Smission platform.

## 1. Assessment Session State Machine
A candidate's assessment session follows a strict, non-reversible lifecycle once completed or abandoned.

```mermaid
stateDiagram-v2
    [*] --> STARTED : User starts assessment (start_session)
    STARTED --> PAUSED : User pauses assessment session
    PAUSED --> RESUMED : User resumes session
    RESUMED --> STARTED
    
    STARTED --> COMPLETED : Submits answer to final question / completes session
    RESUMED --> COMPLETED : Submits answer to final question
    
    STARTED --> ABANDONED : System overrides (e.g. starts a new session for same category)
    PAUSED --> ABANDONED : Session expires or is abandoned
    
    COMPLETED --> [*] : Session data is locked & read-only
    ABANDONED --> [*] : Session terminated without score
```

---

## 2. Event Outbox Lifecycle State Machine
Ensures atomic delivery of events using the transactional Outbox Pattern.

```mermaid
stateDiagram-v2
    [*] --> PENDING : Event written to outbox table (same DB transaction)
    PENDING --> PROCESSING : Worker pulls event for delivery
    PROCESSING --> PROCESSED : Delivery succeeds (2xx response / message broker ACK)
    PROCESSING --> FAILED : Delivery fails after retry limits
    
    FAILED --> PENDING : Manual or automated retry trigger
    PROCESSED --> [*] : Event archived or pruned
    FAILED --> [*] : Alert raised to admin
```
