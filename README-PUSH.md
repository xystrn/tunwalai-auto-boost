# Push Scripts

This repo has 2 GitHub accounts with different cron schedules:

## Accounts

- **shamizen** (original): Runs at minute 19 every hour
- **xystrn** (second): Runs at minute 49 every hour

## How to Push

### Push to shamizen (minute 19)
```bash
./push-to-shamizen.sh
```
or
```bash
git push origin main
```

### Push to xystrn (minute 49)
```bash
./push-to-xystrn.sh
```

This script will:
1. Temporarily change cron to `'49 * * * *'`
2. Commit and push to xystrn
3. Restore cron back to `'19 * * * *'` locally

## Manual Push

If you want to push manually:

```bash
# Push to shamizen
git push origin main

# Push to xystrn (with cron change)
# 1. Edit .github/workflows/auto-boost.yml
# 2. Change cron: '19 * * * *' to cron: '49 * * * *'
# 3. git add .github/workflows/auto-boost.yml
# 4. git commit -m "Change cron to 49"
# 5. git push xystrn main
# 6. Restore cron back to 19 locally
```

## Why Different Cron Schedules?

To avoid both accounts running at the same time and using double the GitHub Actions quota.
- Account 1 runs at :19 (00:19, 01:19, 02:19, ...)
- Account 2 runs at :49 (00:49, 01:49, 02:49, ...)
- 30 minutes apart = efficient quota usage
