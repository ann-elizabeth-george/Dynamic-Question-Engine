# Entity Relationship Diagram (ERD) — Smission Core Engine

Below is the database schema relation diagram using Mermaid syntax, illustrating the primary and foreign keys, relationships, and metadata columns.

```mermaid
erDiagram
    roles {
        int id PK
        string uuid UK
        string name UK
        string description
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    permissions {
        int id PK
        string uuid UK
        string name UK
        string description
        datetime created_at
        datetime updated_at
    }

    role_permissions {
        int role_id PK, FK
        int permission_id PK, FK
        datetime created_at
    }

    users {
        int id PK
        string uuid UK
        string username UK
        string email UK
        string password_hash
        int role_id FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    user_profiles {
        int id PK
        string uuid UK
        int user_id FK, UK
        string first_name
        string last_name
        string phone
        string district_code
        string area_code
        string category_code
        int running_number
        string registration_number UK
        datetime created_at
        datetime updated_at
    }

    registration_counters {
        int id PK
        string uuid UK
        string district_code UK
        string area_code UK
        string category_code UK
        int current_number
        datetime created_at
        datetime updated_at
    }

    categories {
        int id PK
        string uuid UK
        string name UK
        string description
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    questions {
        int id PK
        string uuid UK
        string question_text
        string question_type
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    answers {
        int id PK
        string uuid UK
        int question_id FK
        string answer_text
        boolean is_correct
        int display_order
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    category_question_mappings {
        int id PK
        string uuid UK
        int category_id FK
        int question_id FK
        int display_order
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    assessment_sessions {
        int id PK
        string uuid UK
        int user_id FK
        int category_id FK
        int current_question_index
        int current_question_id FK
        string status
        datetime start_time
        datetime completion_time
        decimal progress_percentage
        datetime created_at
        datetime updated_at
    }

    user_responses {
        int id PK
        string uuid UK
        int session_id FK
        int user_id FK
        int question_id FK
        int answer_id FK
        datetime timestamp
        datetime created_at
        datetime updated_at
    }

    audit_logs {
        int id PK
        string uuid UK
        int user_id FK
        string action
        string target_table
        int target_id
        string old_values
        string new_values
        string ip_address
        string user_agent
        datetime created_at
    }

    event_outbox {
        int id PK
        string uuid UK
        string event_name
        string event_data
        string status
        datetime created_at
        datetime processed_at
    }

    system_settings {
        int id PK
        string uuid UK
        string config_key UK
        string config_value
        string description
        datetime created_at
        datetime updated_at
    }

    roles ||--o{ users : "has"
    roles ||--o{ role_permissions : "maps"
    permissions ||--o{ role_permissions : "maps"
    users ||--|| user_profiles : "profile"
    users ||--o{ assessment_sessions : "starts"
    users ||--o{ user_responses : "submits"
    users ||--o{ audit_logs : "triggers"
    categories ||--o{ category_question_mappings : "defines"
    questions ||--o{ category_question_mappings : "defines"
    questions ||--o{ answers : "has"
    categories ||--o{ assessment_sessions : "evaluated_in"
    assessment_sessions ||--o{ user_responses : "captures"
```
