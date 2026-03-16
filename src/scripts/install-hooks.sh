#!/usr/bin/env bash
# install-hooks.sh  –  Install git hooks for branch enforcement
set -e

HOOK_DIR=".git/hooks"
SCRIPTS_DIR="src/scripts"

if [ ! -d "$HOOK_DIR" ]; then
  echo "❌  Not inside a git repository. Run from project root."
  exit 1
fi

echo "📦  Installing git hooks..."

cp "$SCRIPTS_DIR/pre-push" "$HOOK_DIR/pre-push"
chmod +x "$HOOK_DIR/pre-push"

echo "✅  pre-push hook installed at $HOOK_DIR/pre-push"
echo ""
echo "The hook will now block any 'git push' from non-compliant branch names."
echo "To test:  python src/main/python/branch_enforcer.py current"
