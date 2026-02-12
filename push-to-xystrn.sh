#!/bin/bash
# Script to push to xystrn account with cron schedule changed to minute 49

echo "=== Push to xystrn account ==="
echo ""

# 1. Backup current workflow file
echo "1. Backing up current workflow..."
cp .github/workflows/auto-boost.yml .github/workflows/auto-boost.yml.backup

# 2. Change cron schedule to minute 49
echo "2. Changing cron schedule to minute 49..."
sed -i "s/cron: '[0-9]* \* \* \* \*'/cron: '49 * * * *'/g" .github/workflows/auto-boost.yml

# 3. Show the change
echo "3. Verifying change..."
grep "cron:" .github/workflows/auto-boost.yml

# 4. Commit the change
echo "4. Committing change..."
git add .github/workflows/auto-boost.yml
git commit -m "Change cron schedule to minute 49 for xystrn account"

# 5. Push to xystrn
echo "5. Pushing to xystrn..."
git push xystrn main

# 6. Restore original workflow file
echo "6. Restoring original workflow..."
mv .github/workflows/auto-boost.yml.backup .github/workflows/auto-boost.yml
git add .github/workflows/auto-boost.yml
git commit -m "Restore cron schedule to minute 19"

echo ""
echo "=== Done! ==="
echo "- Pushed to xystrn with cron: '49 * * * *'"
echo "- Local repo restored to cron: '19 * * * *'"
