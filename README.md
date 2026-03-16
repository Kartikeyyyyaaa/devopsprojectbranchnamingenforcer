# Branch Naming Convention Enforcer

**Student Name:** Kartikeya Aryan Mishra  
**Registration No:** 23FE10CSE00736  
**Course:** CSE3253 DevOps [PE6]  
**Semester:** VI (2025–2026)  
**Project Type:** Git & Agile  
**Difficulty:** Intermediate  

---

## 📌 Project Overview

### Problem Statement
Teams working on shared repositories often use inconsistent branch names like `my-work`, `BUGFIX`, `test123`, or `feature_login`, making it impossible to understand branch purpose at a glance, breaking CI/CD automation that relies on branch prefixes, and causing confusion in code reviews.

### Objectives
- [x] Build a CLI tool that validates branch names against configurable conventions
- [x] Provide actionable suggestions when a branch name is invalid
- [x] Integrate enforcement as a Git pre-push hook to block non-compliant pushes
- [x] Automate validation in CI/CD (Jenkins + GitHub Actions)
- [x] Support batch auditing of all branches in a repository

### Key Features
- ✅ Real-time branch name validation with clear pass/fail output
- 💡 Smart fix suggestions for invalid names
- 🔒 Git pre-push hook integration to block bad branches at source
- 🔍 Full repository audit command (`audit`)
- 🐳 Fully containerised with Docker
- 🤖 Automated CI via GitHub Actions and Jenkins

---

## 🛠️ Technology Stack

### Core Technologies
- **Language:** Python 3.11
- **Framework:** stdlib only (no external runtime deps)
- **Database:** None

### DevOps Tools
- **Version Control:** Git
- **CI/CD:** Jenkins + GitHub Actions
- **Containerisation:** Docker
- **Orchestration:** Kubernetes
- **Config Management:** Puppet
- **Monitoring:** Nagios

---

## 🚀 Getting Started

### Prerequisites
- [ ] Docker Desktop v20.10+
- [ ] Git 2.30+
- [ ] Python 3.8+

### Quick Start with Docker

```bash
# 1. Clone the repo
git clone https://github.com/kartikeya/devopsprojectbranchnamingenforcer.git
cd devopsprojectbranchnamingenforcer

# 2. Build & run
docker build -t branch-enforcer:latest -f infrastructure/docker/Dockerfile .

# 3. Validate a branch name
docker run --rm branch-enforcer:latest validate "feature/my-login-page"

# 4. Show all rules
docker run --rm branch-enforcer:latest rules
```

### Without Docker

```bash
# Clone & enter
git clone https://github.com/kartikeya/devopsprojectbranchnamingenforcer.git
cd devopsprojectbranchnamingenforcer

# Install test deps (runtime has none)
pip install -r requirements.txt

# Validate a branch
python src/main/python/branch_enforcer.py validate "feature/my-login-page"

# Audit all branches in your repo
python src/main/python/branch_enforcer.py audit

# Show rules
python src/main/python/branch_enforcer.py rules
```

### Install Git Hook (Recommended)

```bash
bash src/scripts/install-hooks.sh
```

After installing, any `git push` from a non-compliant branch will be **automatically blocked**.

---

## 📂 Project Structure

```
devopsprojectbranchnamingenforcer/
│
├── src/
│   ├── main/python/
│   │   └── branch_enforcer.py     ← Core CLI tool
│   ├── config/
│   │   └── config.json            ← Convention rules
│   └── scripts/
│       ├── pre-push               ← Git hook
│       └── install-hooks.sh       ← Hook installer
│
├── tests/
│   ├── unit/test_branch_enforcer.py
│   └── integration/test_cli.py
│
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   └── configmap.yaml
│   └── puppet/branch_enforcer.pp
│
├── pipelines/
│   ├── Jenkinsfile
│   └── .github/workflows/cicd.yml
│
├── monitoring/nagios/branch_enforcer.cfg
├── docs/
├── requirements.txt
└── README.md
```

---

## 📋 Branch Naming Rules

| Type       | Pattern                        | Example                        |
|------------|-------------------------------|-------------------------------|
| feature    | `feature/<slug>`               | `feature/user-authentication` |
| fix        | `fix/<slug>`                   | `fix/login-null-pointer`      |
| hotfix     | `hotfix/<slug>`                | `hotfix/critical-db-crash`    |
| release    | `release/v<major.minor.patch>` | `release/v1.2.0`              |
| docs       | `docs/<slug>`                  | `docs/api-reference-update`   |
| refactor   | `refactor/<slug>`              | `refactor/payment-module`     |
| test       | `test/<slug>`                  | `test/selenium-dashboard`     |
| chore      | `chore/<slug>`                 | `chore/update-dependencies`   |
| protected  | `main / master / develop`      | `main`                        |

**Rules:** lowercase only · hyphens only (no underscores/spaces) · 3–50 chars after prefix

---

## ⚙️ CLI Usage

```bash
# Validate a single branch
python src/main/python/branch_enforcer.py validate "feature/my-feature"

# Validate current checked-out branch
python src/main/python/branch_enforcer.py current

# Audit all local branches
python src/main/python/branch_enforcer.py audit

# Batch validate from file (one branch per line)
python src/main/python/branch_enforcer.py batch branches.txt

# Show all rules
python src/main/python/branch_enforcer.py rules
```

---

## 🧪 Testing

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# With coverage
pytest tests/ --cov=src/main/python --cov-report=term-missing
```

**Target coverage: > 80%**

---

## 🔄 CI/CD Pipeline

### Stages
1. **Code Quality** – flake8 linting
2. **Unit Tests** – 20+ test cases with pytest
3. **Integration Tests** – CLI end-to-end tests
4. **Build Docker Image** – containerise the tool
5. **Security Scan** – Trivy image vulnerability scan
6. **Validate Branch Name** – the tool validates itself in CI
7. **Deploy to Staging** – on `main` branch pushes

---

## 📊 Performance Metrics

| Metric             | Target   | Current        |
|--------------------|----------|----------------|
| Build Time         | < 2 min  | ~45 sec        |
| Test Coverage      | > 80%    | ~90%           |
| Validation Speed   | < 100ms  | < 10ms         |
| Deployment Freq.   | On push  | Automated      |

---

## 🐳 Docker & Kubernetes

```bash
# Build
docker build -t branch-enforcer:latest -f infrastructure/docker/Dockerfile .

# Validate a branch
docker run --rm branch-enforcer:latest validate "feature/my-feature"

# Kubernetes
kubectl apply -f infrastructure/kubernetes/
kubectl get pods
```

---

## 🔒 Security

- No external runtime dependencies
- Input validated with strict regex (no injection surface)
- Trivy scan on every CI build
- Config via JSON (no secrets required)

---

## 🏆 Project Challenges

1. **Regex edge cases** – `release/v1.2.0` vs `release/1.2.0` – solved with strict semver pattern
2. **Git hook portability** – different shell environments; solved by writing hook in Python
3. **CI self-validation** – the CI pipeline validates its own branch, requiring graceful non-blocking output

## 💡 Learnings
- Git hooks are powerful low-friction enforcement points
- Regex patterns must be anchored (`^...$`) to prevent partial matches
- Exit codes matter – CI tools rely on them to pass/fail stages

---

## 📚 Documentation

- [Design Document](docs/designdocument.md)
- [User Guide](docs/userguide.md)

---

## 👤 Contact

**Student:** Kartikeya Aryan Mishra  
**Reg No:** 23FE10CSE00736  
**Course Coordinator:** Mr. Jay Shankar Sharma  
**Consultation Hours:** Thursday & Friday, 5–6 PM, LHC 308F
