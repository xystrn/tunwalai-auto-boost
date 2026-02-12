#!/bin/bash
# Script to push to shamizen account (original) with cron schedule at minute 19

echo "=== Push to shamizen account (original) ==="
echo ""

# 1. Verify cron schedule is at minute 19
echo "1. Verifying cron schedule..."
grep "cron:" .github/workflows/auto-boost.yml

# 2. Push to origin (shamizen)
echo "2. Pushing to shamizen..."
git push origin main

echo ""
echo "=== Done! ==="
echo "- Pushed to shamizen with cron: '19 * * * *'"
