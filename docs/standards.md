# Development & Deployment Standards — Smission Core Engine

## 1. Coding Standards

### 1.2. Backend (FastAPI / Python)
- **Style Guide**: Strictly adhere to **PEP 8**. Use `ruff` or `flake8` for linting.
- **Type Hints**: Mandatory for all function parameters, return types, and variables.
- **Async vs Sync**: Use standard `def` for database block operations using SQLAlchemy sessions, and `async def` for endpoints requiring parallel network I/O.
- **Error Handling**: Never return bare exceptions. Use FastAPI `HTTPException` with clear status codes and descriptions.

### 1.3. Frontend (React / JavaScript)
- **Component Design**: Use functional components with hooks.
- **Formatting**: Format using Prettier.
- **Folder Structure**: Group pages under `pages/`, shared elements under `components/`, contexts under `context/`, layouts under `layouts/`.

---

## 2. Naming Conventions

| Component | Convention | Example |
| :--- | :--- | :--- |
| **Python Classes** | PascalCase | `AssessmentEngine` |
| **Python Functions/Variables** | snake_case | `submit_answer` |
| **JS Components/Files** | PascalCase | `AdminCategories.jsx` |
| **JS Functions/Variables** | camelCase | `loadCategories` |
| **Database Tables** | snake_case (plural) | `assessment_sessions` |
| **Database Columns** | snake_case | `created_at` |

---

## 3. Git Branch Strategy
We use a **Trunk-Based Development** model with short-lived feature branches:

```
main  ───────────────────────────────────────────────────► (Production)
       ▲             ▲                      ▲
       │             │                      │
feat/db-refactor  feat/auth-module  feat/assessment-engine (Short-lived)
```

1. **Main Branch**: Always deployable to production.
2. **Feature Branches**: Created from `main`, named as `feat/feature-name` or `fix/bug-name`.
3. **Pull Requests**: Rebased onto `main` and merged after automated linting and tests pass.

---

## 4. CI/CD Pipeline Specification
Our pipeline automates testing, packaging, and deployments to Google Cloud Run:

```yaml
name: Smission CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt pytest httpx
      - name: Run Linter (Ruff)
        run: pip install ruff && ruff check backend
      - name: Run Tests
        run: pytest backend/app/tests

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Auth to GCP
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - name: Deploy to Cloud Run (Backend)
        run: |
          gcloud run deploy smission-backend \
            --source ./backend \
            --region us-central1 \
            --allow-unauthenticated
```
