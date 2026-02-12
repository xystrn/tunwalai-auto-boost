---
inclusion: auto
---

# Multi-Account Push Strategy

This repository maintains code on two GitHub accounts with different GitHub Actions cron schedules.

## Accounts & Cron Schedules

1. **shamizen** (origin remote) - Cron: `'19 * * * *'` (runs at minute 19 every hour)
2. **xystrn** (xystrn remote) - Cron: `'49 * * * *'` (runs at minute 49 every hour)

## Default Push Behavior

**When user says "push" without specifying account:**
- Push to BOTH accounts sequentially
- Follow the complete workflow below

## Complete Push Workflow (Both Accounts)

### Step 1: Push to shamizen (origin)
1. Ensure `.github/workflows/auto-boost.yml` has cron: `'19 * * * *'`
2. Stage all changes: `git add -A`
3. Commit if there are changes
4. Push to origin: `git push origin main`

### Step 2: Push to xystrn
1. Change `.github/workflows/auto-boost.yml` cron to `'49 * * * *'` using `strReplace`
2. Stage the workflow file: `git add .github/workflows/auto-boost.yml`
3. Commit: "Update cron schedule to 49 minutes for xystrn account"
4. Push to xystrn: `git push xystrn main` (use `--force` if needed)

### Step 3: Restore local state
1. Change cron back to `'19 * * * *'` using `strReplace`
2. Commit: "Restore cron to 19 minutes for shamizen"
3. This keeps local repo in sync with shamizen (origin)

## Single Account Push

### Push to shamizen only
**Trigger:** "push to shamizen", "push shamizen", "push to origin"
- Follow Step 1 only

### Push to xystrn only
**Trigger:** "push to xystrn", "push xystrn"
- Follow Steps 2 and 3 only

## Critical Rules

- ALWAYS use `strReplace` tool for editing `.github/workflows/auto-boost.yml`
- NEVER use sed, awk, or command-line text editing
- Local repository should always maintain cron at `'19 * * * *'` (shamizen's schedule)
- Only temporarily change to `'49 * * * *'` when pushing to xystrn, then restore immediately

## Example strReplace Usage

```
To change to xystrn cron:
oldStr: "    - cron: '19 * * * *'"
newStr: "    - cron: '49 * * * *'"

To restore to shamizen cron:
oldStr: "    - cron: '49 * * * *'"
newStr: "    - cron: '19 * * * *'"
```
