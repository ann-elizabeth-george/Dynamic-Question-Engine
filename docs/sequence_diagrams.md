# Sequence Diagrams — Smission Core Engine

This document contains sequence diagrams for critical operations in the Core Engine using Mermaid.

## 1. Candidate Transactional Registration & Registration Number Generation

This diagram illustrates how Phase 4 (Registration Engine) and Phase 5 (Registration Number Service) operate transactionally.

```mermaid
sequenceDiagram
    autonumber
    actor Candidate
    participant API as API Layer
    participant RegService as RegistrationService
    participant RegNumService as RegistrationNumberService
    participant DB as PostgreSQL DB
    participant Outbox as Event Outbox

    Candidate->>API: POST /api/v1/auth/register (Username, Email, Password)
    API->>RegService: register_user()
    activate RegService
    RegService->>DB: INSERT INTO users
    DB-->>RegService: Return user_id
    RegService->>DB: INSERT INTO event_outbox (USER_REGISTERED)
    RegService-->>API: Return user object
    deactivate RegService
    API-->>Candidate: Registration successful, tokens returned

    Candidate->>API: POST /api/v1/profile (Profile info, district, area, category)
    API->>RegService: create_user_profile(user_id, profile_data)
    activate RegService
    RegService->>DB: Begin Transaction
    RegService->>RegNumService: generate_registration_number(district, area, category)
    activate RegNumService
    RegNumService->>DB: SELECT * FROM registration_counters WHERE ... FOR UPDATE (Row Lock)
    alt Counter does not exist
        RegNumService->>DB: INSERT INTO registration_counters (current_number=1)
    else Counter exists
        RegNumService->>DB: UPDATE registration_counters SET current_number = current_number + 1
    end
    RegNumService-->>RegService: Return generated reg number (e.g. 01-A-ST-001)
    deactivate RegNumService
    RegService->>DB: INSERT INTO user_profiles (registration_number, ...)
    RegService->>DB: INSERT INTO event_outbox (PROFILE_COMPLETED)
    RegService->>DB: Commit Transaction
    RegService-->>API: Return profile object
    deactivate RegService
    API-->>Candidate: Profile saved with Registration Number
```

---

## 2. Assessment Session Flow & Answer Submission

This diagram details the navigation and strategy execution for question delivery.

```mermaid
sequenceDiagram
    autonumber
    actor Candidate
    participant API as API Layer
    participant AssessmentService as AssessmentService
    participant Engine as AssessmentEngine (Ordered Strategy)
    participant DB as PostgreSQL DB
    
    Candidate->>API: POST /api/v1/assessment/submit-answer (session_id, question_id, answer_id)
    API->>AssessmentService: submit_answer(user_id, session_id, question_id, answer_id)
    activate AssessmentService
    AssessmentService->>DB: Begin Transaction
    AssessmentService->>DB: Validate session_id is ACTIVE
    AssessmentService->>DB: Validate answer_id belongs to question_id
    AssessmentService->>DB: INSERT / UPDATE user_responses
    AssessmentService->>DB: Query category_question_mappings for category
    DB-->>AssessmentService: Return mappings list
    
    AssessmentService->>Engine: get_next_question_details(mappings, current_index)
    activate Engine
    Note over Engine: Calculates next display order index
    Engine-->>AssessmentService: Returns (is_completed, next_index, next_q_id)
    deactivate Engine
    
    alt is_completed = True
        AssessmentService->>DB: UPDATE assessment_sessions SET status = 'COMPLETED', progress = 100.0
        AssessmentService->>DB: INSERT INTO event_outbox (ASSESSMENT_COMPLETED)
    else is_completed = False
        AssessmentService->>DB: UPDATE assessment_sessions SET current_question_index = next_index, current_question_id = next_q_id, progress = calculated_progress
    end
    
    AssessmentService->>DB: INSERT INTO event_outbox (QUESTION_ANSWERED)
    AssessmentService->>DB: Commit Transaction
    AssessmentService-->>API: Return next_question / completion status
    deactivate AssessmentService
    API-->>Candidate: Answer registered, returned next state
```
