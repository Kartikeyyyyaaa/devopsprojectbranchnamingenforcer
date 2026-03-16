# Technical Design Document
## Branch Naming Convention Enforcer

**Author:** Kartikeya Aryan Mishra (23FE10CSE00736)  
**Version:** 1.0.0  
**Date:** March 2026  

---

## 1. Overview

The Branch Naming Convention Enforcer is a Python CLI tool and Git hook system that validates branch names against a configurable set of regex patterns. It integrates with local Git workflows and remote CI/CD pipelines.

---

## 2. Architecture

```
 Developer workstation
 ┌─────────────────────────────────────┐
 │  git push  →  pre-push hook         │
 │                  ↓                  │
 │         branch_enforcer.py          │
 │         validate(branch_name)       │
 │              ↓       ↓              │
 │           PASS     FAIL → blocked   │
 └─────────────────────────────────────┘

 CI/CD (GitHub Actions / Jenkins)
 ┌─────────────────────────────────────┐
 │  Push event → workflow triggered    │
 │  → lint → test → build → scan      │
 │  → validate-branch stage           │
 └─────────────────────────────────────┘
```

---

## 3. Core Components

### 3.1 BranchEnforcer class
- `validate(branch)` → dict with `valid`, `type`, `message`, `suggestion`
- `validate_many(branches)` → list of results
- `audit_repo()` → full repo audit via `git branch`
- `get_current_branch()` → subprocess call to git

### 3.2 CLI (argparse)
Commands: `validate`, `batch`, `audit`, `current`, `rules`

### 3.3 Git Hook
`src/scripts/pre-push` – Python script installed to `.git/hooks/pre-push`

---

## 4. Pattern Design

All patterns are anchored (`^...$`) to prevent partial matches.

| Type    | Regex |
|---------|-------|
| feature | `^feature/[a-z0-9][a-z0-9\-]{2,48}$` |
| fix     | `^fix/[a-z0-9][a-z0-9\-]{2,48}$` |
| release | `^release/v\d+\.\d+\.\d+$` |
| main    | `^(main\|master\|develop)$` |

---

## 5. Exit Codes

| Code | Meaning |
|------|---------|
| 0    | All branches valid |
| 1    | One or more branches invalid |

---

## 6. Extensibility

Custom patterns can be added via `src/config/config.json` under `"custom_patterns"` without modifying source code.
