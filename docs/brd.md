# Business Requirements Document (BRD) — Smission Core Engine

## 1. Project Overview
The **Smission Core Engine** is an enterprise-grade, high-performance assessment platform designed to deliver dynamic, structured, and rules-based assessments to candidates. The system supports multi-tenant user categorization, thread-safe transactional registration, dynamic question routing, audit logging, and transactional event dispatching.

---

## 2. Objectives & Scope
- **Transactional Candidate Registration**: Candidates select a Category, fill in a profile, and obtain a thread-safe, sequential registration number unique to their region.
- **Dynamic Question Library**: Admin-managed library supporting multiple question formats (single choice, multiple choice, boolean, open text, date/number responses).
- **Extensible Assessment Engine**: Deliver questions based on active mappings with support for multiple strategies (e.g. Ordered, Rule-Based, Adaptive).
- **Enterprise Operations**: Fully audited tables and event-driven data propagation using the Outbox pattern.

---

## 3. Key Stakeholders & Roles
- **System Administrator (Admin)**: Responsible for managing roles, users, categories, question-answer banks, mapping matrices, and reviewing audit logs.
- **Candidate (Student)**: Enrolls in a specific category, enters profile information, takes assessments, views completion status, and history.

---

## 4. Functional Requirements

### 4.1. Account & Profile Management
- **Account Registration**: Standard email, username, and password verification.
- **Transactional Profile Completion**: Includes fields for first name, last name, phone, district code, area code, and category code.
- **Registration Number Generation**: 
  - Format: `{district_code}-{area_code}-{category_code}-{running_number}` (e.g. `01-A-ST-003`).
  - Thread safety must be guaranteed via table-level locks (`SELECT FOR UPDATE`) on the registration counter to avoid number duplication.

### 4.2. Assessment Session Flow
- **Session Lifecycle**: Candidates can start, resume, pause, complete, or abandon assessment sessions.
- **Navigation Engine**: Calculates the current, next, and previous question based on category mapping.
- **Response Mutability**: Candidates can update answers while the session is active. Once the session is marked as `COMPLETED`, all responses become read-only and locked.

---

## 5. Non-Functional Requirements
- **Security**: Data protection using JWT bearer tokens, encrypted passwords (bcrypt), and role-based access control (RBAC).
- **Scalability**: Sub-second API response times and support for high concurrent registration queries.
- **Auditability**: Complete tracking of record changes (old values, new values, timestamp, user context).
