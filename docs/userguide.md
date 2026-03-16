# User Guide – Branch Naming Convention Enforcer

## Installation

```bash
git clone https://github.com/kartikeya/devopsprojectbranchnamingenforcer.git
cd devopsprojectbranchnamingenforcer
pip install -r requirements.txt
bash src/scripts/install-hooks.sh   # installs the git pre-push hook
```

## Daily Usage

### Check a branch before creating it
```bash
python src/main/python/branch_enforcer.py validate "feature/my-new-feature"
```

**Valid output:**
```
=======================================================
  Branch : feature/my-new-feature
  Status : ✅  Valid branch name! Type: feature
  Type   : feature
=======================================================
```

**Invalid output:**
```
=======================================================
  Branch : Feature/MyNewFeature
  Status : ❌  'Feature/MyNewFeature' does not follow naming conventions.
  Tip    : Try: feature/mynewfeature
=======================================================
```

### Show all rules
```bash
python src/main/python/branch_enforcer.py rules
```

### Audit your entire repo
```bash
python src/main/python/branch_enforcer.py audit
```

### Validate current branch
```bash
python src/main/python/branch_enforcer.py current
```

### Batch validate from a file
```bash
# Create branches.txt with one name per line
python src/main/python/branch_enforcer.py batch branches.txt
```

## Naming Quick Reference

| ✅ Valid                        | ❌ Invalid              |
|--------------------------------|------------------------|
| `feature/user-auth`            | `Feature/UserAuth`     |
| `fix/null-pointer`             | `fix_null_pointer`     |
| `release/v2.1.0`               | `release/2.1.0`        |
| `hotfix/db-crash`              | `hotfix/DB Crash`      |
| `main`                         | `my-branch`            |
