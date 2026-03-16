#!/usr/bin/env python3
"""
Integration tests – CLI behaviour end-to-end.
Run: pytest tests/integration/test_cli.py -v
"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src/main/python"))

import pytest

CLI = [sys.executable,
       os.path.join(os.path.dirname(__file__),
                    "../../src/main/python/branch_enforcer.py")]


def run_cli(*args):
    result = subprocess.run(CLI + list(args),
                            capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


class TestCLIValidate:
    def test_valid_branch_exit_0(self):
        code, out = run_cli("validate", "feature/new-login")
        assert code == 0
        assert "✅" in out

    def test_invalid_branch_exit_1(self):
        code, out = run_cli("validate", "INVALID_BRANCH")
        assert code == 1
        assert "❌" in out

    def test_suggestion_shown(self):
        code, out = run_cli("validate", "Feature/UserLogin")
        assert "Try:" in out or "tip" in out.lower() or "suggest" in out.lower()


class TestCLIRules:
    def test_rules_output(self):
        code, out = run_cli("rules")
        assert code == 0
        assert "feature" in out
        assert "release" in out


class TestCLIBatch:
    def test_batch_file(self, tmp_path):
        f = tmp_path / "branches.txt"
        f.write_text("feature/valid\nINVALID\nfix/also-valid\n")
        code, out = run_cli("batch", str(f))
        assert "✅" in out
        assert "❌" in out
        assert code == 1  # at least one invalid

    def test_batch_all_valid(self, tmp_path):
        f = tmp_path / "branches.txt"
        f.write_text("feature/ok\nfix/also-ok\n")
        code, _ = run_cli("batch", str(f))
        assert code == 0
