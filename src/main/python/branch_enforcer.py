#!/usr/bin/env python3
"""
Branch Naming Convention Enforcer
Author: Kartikeya Aryan Mishra
Reg No: 23FE10CSE00736
Course: CSE3253 DevOps [PE6]
"""

import re
import sys
import json
import argparse
import subprocess
from datetime import datetime, timezone
from typing import Optional


# ──────────────────────────────────────────────
#  Convention Rules
# ──────────────────────────────────────────────
BRANCH_PATTERNS = {
    "feature":  r"^feature/[a-z0-9][a-z0-9\-]{2,48}$",
    "fix":      r"^fix/[a-z0-9][a-z0-9\-]{2,48}$",
    "hotfix":   r"^hotfix/[a-z0-9][a-z0-9\-]{2,48}$",
    "release":  r"^release/v\d+\.\d+\.\d+$",
    "docs":     r"^docs/[a-z0-9][a-z0-9\-]{2,48}$",
    "refactor": r"^refactor/[a-z0-9][a-z0-9\-]{2,48}$",
    "test":     r"^test/[a-z0-9][a-z0-9\-]{2,48}$",
    "chore":    r"^chore/[a-z0-9][a-z0-9\-]{2,48}$",
    "main":     r"^(main|master|develop)$",
}

EXAMPLES = {
    "feature":  "feature/user-authentication",
    "fix":      "fix/login-null-pointer",
    "hotfix":   "hotfix/critical-db-crash",
    "release":  "release/v1.2.0",
    "docs":     "docs/api-reference-update",
    "refactor": "refactor/payment-module",
    "test":     "test/selenium-dashboard",
    "chore":    "chore/update-dependencies",
    "main":     "main  /  master  /  develop",
}


class BranchEnforcer:
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.patterns = BRANCH_PATTERNS.copy()
        # Merge custom patterns from config if any
        if self.config.get("custom_patterns"):
            self.patterns.update(self.config["custom_patterns"])

    def _load_config(self, path: Optional[str]) -> dict:
        if path:
            try:
                with open(path) as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        return {}

    # ── Core validation ──────────────────────
    def validate(self, branch_name: str) -> dict:
        result = {
            "branch":    branch_name,
            "valid":     False,
            "type":      None,
            "message":   "",
            "suggestion": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if not branch_name or not branch_name.strip():
            result["message"] = "❌  Branch name cannot be empty."
            return result

        branch_name = branch_name.strip()

        for btype, pattern in self.patterns.items():
            if re.match(pattern, branch_name):
                result["valid"] = True
                result["type"]  = btype
                result["message"] = f"✅  Valid branch name! Type: {btype}"
                return result

        # Invalid – build helpful feedback
        result["message"] = f"❌  '{branch_name}' does not follow naming conventions."
        result["suggestion"] = self._suggest(branch_name)
        return result

    def _suggest(self, branch_name: str) -> str:
        lower = branch_name.lower()
        for prefix in ("feature", "fix", "hotfix", "release", "docs",
                       "refactor", "test", "chore"):
            if lower.startswith(prefix):
                slug = re.sub(r"[^a-z0-9\-]", "-",
                              re.sub(r"[_/\s]+", "-", lower))
                slug = re.sub(r"-{2,}", "-", slug).strip("-")
                return f"Try: {prefix}/{slug.replace(prefix+'-', '', 1)}"
        clean = re.sub(r"[^a-z0-9\-]", "-",
                       re.sub(r"[_\s]+", "-", lower)).strip("-")
        return f"Try: feature/{clean}  (or another valid prefix)"

    # ── Batch validate ───────────────────────
    def validate_many(self, branches: list[str]) -> list[dict]:
        return [self.validate(b) for b in branches]

    # ── Git integration ──────────────────────
    def get_current_branch(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def list_local_branches(self) -> list[str]:
        try:
            result = subprocess.run(
                ["git", "branch", "--format=%(refname:short)"],
                capture_output=True, text=True, check=True
            )
            return [b.strip() for b in result.stdout.splitlines() if b.strip()]
        except subprocess.CalledProcessError:
            return []

    def audit_repo(self) -> dict:
        branches = self.list_local_branches()
        if not branches:
            return {"error": "Not a git repo or no branches found."}
        results   = self.validate_many(branches)
        valid     = [r for r in results if r["valid"]]
        invalid   = [r for r in results if not r["valid"]]
        return {
            "total":   len(branches),
            "valid":   len(valid),
            "invalid": len(invalid),
            "details": results,
            "score":   f"{round(len(valid)/len(branches)*100)}%",
        }

    # ── Pretty print ─────────────────────────
    @staticmethod
    def print_result(result: dict):
        print(f"\n{'='*55}")
        print(f"  Branch : {result['branch']}")
        print(f"  Status : {result['message']}")
        if result.get("type"):
            print(f"  Type   : {result['type']}")
        if result.get("suggestion"):
            print(f"  Tip    : {result['suggestion']}")
        print(f"{'='*55}\n")

    @staticmethod
    def print_rules():
        print("\n📋  Allowed Branch Naming Conventions")
        print("─" * 55)
        for btype, example in EXAMPLES.items():
            print(f"  {btype:<10}  →  {example}")
        print("\nRules:")
        print("  • Use lowercase letters, numbers, and hyphens only")
        print("  • No spaces, underscores, or uppercase letters")
        print("  • 3–50 characters after the prefix/")
        print("  • release branches must follow semver: v1.2.3\n")


# ──────────────────────────────────────────────
#  CLI
# ──────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="branch-enforcer",
        description="Branch Naming Convention Enforcer – CSE3253 DevOps Project"
    )
    sub = p.add_subparsers(dest="command")

    # validate
    v = sub.add_parser("validate", help="Validate a single branch name")
    v.add_argument("branch", help="Branch name to validate")

    # batch
    b = sub.add_parser("batch", help="Validate multiple branch names from a file")
    b.add_argument("file", help="Text file with one branch name per line")

    # audit
    sub.add_parser("audit", help="Audit all branches in the current git repo")

    # current
    sub.add_parser("current", help="Validate the currently checked-out branch")

    # rules
    sub.add_parser("rules", help="Display all naming convention rules")

    return p


def main():
    parser = build_parser()
    args   = parser.parse_args()
    enforcer = BranchEnforcer()

    if args.command == "validate":
        result = enforcer.validate(args.branch)
        BranchEnforcer.print_result(result)
        sys.exit(0 if result["valid"] else 1)

    elif args.command == "batch":
        try:
            with open(args.file) as f:
                branches = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌  File not found: {args.file}")
            sys.exit(1)
        results = enforcer.validate_many(branches)
        for r in results:
            BranchEnforcer.print_result(r)
        invalid_count = sum(1 for r in results if not r["valid"])
        sys.exit(1 if invalid_count else 0)

    elif args.command == "audit":
        audit = enforcer.audit_repo()
        if "error" in audit:
            print(f"❌  {audit['error']}")
            sys.exit(1)
        print(f"\n{'='*55}")
        print(f"  🔍  Repository Branch Audit")
        print(f"{'='*55}")
        print(f"  Total branches : {audit['total']}")
        print(f"  Valid          : {audit['valid']}")
        print(f"  Invalid        : {audit['invalid']}")
        print(f"  Compliance     : {audit['score']}")
        print(f"{'─'*55}")
        for r in audit["details"]:
            status = "✅" if r["valid"] else "❌"
            print(f"  {status}  {r['branch']}")
            if r.get("suggestion"):
                print(f"       💡 {r['suggestion']}")
        print(f"{'='*55}\n")
        sys.exit(1 if audit["invalid"] else 0)

    elif args.command == "current":
        branch = enforcer.get_current_branch()
        if not branch:
            print("❌  Could not determine current branch.")
            sys.exit(1)
        result = enforcer.validate(branch)
        BranchEnforcer.print_result(result)
        sys.exit(0 if result["valid"] else 1)

    elif args.command == "rules":
        BranchEnforcer.print_rules()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
