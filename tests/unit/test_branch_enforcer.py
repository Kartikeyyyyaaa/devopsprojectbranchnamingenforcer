#!/usr/bin/env python3
"""
Unit tests for Branch Naming Convention Enforcer
Run: pytest tests/unit/test_branch_enforcer.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src/main/python"))

import pytest
from branch_enforcer import BranchEnforcer


@pytest.fixture
def enforcer():
    return BranchEnforcer()


# ── Valid branch names ────────────────────────────────────────
class TestValidBranches:
    def test_feature_branch(self, enforcer):
        r = enforcer.validate("feature/user-authentication")
        assert r["valid"] is True
        assert r["type"] == "feature"

    def test_fix_branch(self, enforcer):
        r = enforcer.validate("fix/login-null-pointer")
        assert r["valid"] is True
        assert r["type"] == "fix"

    def test_hotfix_branch(self, enforcer):
        r = enforcer.validate("hotfix/critical-db-crash")
        assert r["valid"] is True
        assert r["type"] == "hotfix"

    def test_release_semver(self, enforcer):
        r = enforcer.validate("release/v1.2.0")
        assert r["valid"] is True
        assert r["type"] == "release"

    def test_docs_branch(self, enforcer):
        r = enforcer.validate("docs/api-reference-update")
        assert r["valid"] is True

    def test_refactor_branch(self, enforcer):
        r = enforcer.validate("refactor/payment-module")
        assert r["valid"] is True

    def test_test_branch(self, enforcer):
        r = enforcer.validate("test/selenium-dashboard")
        assert r["valid"] is True

    def test_chore_branch(self, enforcer):
        r = enforcer.validate("chore/update-dependencies")
        assert r["valid"] is True

    def test_main_branch(self, enforcer):
        assert enforcer.validate("main")["valid"] is True

    def test_master_branch(self, enforcer):
        assert enforcer.validate("master")["valid"] is True

    def test_develop_branch(self, enforcer):
        assert enforcer.validate("develop")["valid"] is True


# ── Invalid branch names ──────────────────────────────────────
class TestInvalidBranches:
    def test_uppercase_letters(self, enforcer):
        assert enforcer.validate("Feature/User-Auth")["valid"] is False

    def test_spaces_in_name(self, enforcer):
        assert enforcer.validate("feature/user auth")["valid"] is False

    def test_underscores(self, enforcer):
        assert enforcer.validate("feature/user_auth")["valid"] is False

    def test_missing_prefix(self, enforcer):
        assert enforcer.validate("user-authentication")["valid"] is False

    def test_wrong_release_format(self, enforcer):
        assert enforcer.validate("release/1.2.0")["valid"] is False  # missing 'v'

    def test_empty_string(self, enforcer):
        assert enforcer.validate("")["valid"] is False

    def test_only_prefix(self, enforcer):
        assert enforcer.validate("feature/")["valid"] is False

    def test_double_slashes(self, enforcer):
        assert enforcer.validate("feature//login")["valid"] is False

    def test_unknown_prefix(self, enforcer):
        assert enforcer.validate("wip/my-work")["valid"] is False


# ── Suggestion quality ────────────────────────────────────────
class TestSuggestions:
    def test_suggestion_provided_for_invalid(self, enforcer):
        r = enforcer.validate("Feature/UserLogin")
        assert r["suggestion"] != ""

    def test_suggestion_starts_with_try(self, enforcer):
        r = enforcer.validate("feature_user_login")
        assert r["suggestion"].startswith("Try:")


# ── Batch validation ──────────────────────────────────────────
class TestBatchValidation:
    def test_batch_mixed(self, enforcer):
        branches = [
            "feature/valid-branch",
            "INVALID_BRANCH",
            "fix/another-valid",
        ]
        results = enforcer.validate_many(branches)
        assert len(results) == 3
        assert results[0]["valid"] is True
        assert results[1]["valid"] is False
        assert results[2]["valid"] is True

    def test_batch_all_valid(self, enforcer):
        branches = ["feature/a-b-c", "fix/x-y-z", "main"]
        results = enforcer.validate_many(branches)
        assert all(r["valid"] for r in results)
