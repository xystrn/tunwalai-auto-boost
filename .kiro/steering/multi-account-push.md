---
inclusion: auto
---

# Multi-Account Push Strategy

This repository syncs to two GitHub accounts with different cron schedules.

## Account Mapping

- **shamizen** (origin remote) → cron: `'19 * * * *'`
- **xystrn** (xystrn remote) → cron: `'49 * * * *'`

## Push Workflow

### Push to shamizen
1. Check cron in `.github/workflows/auto-boost.yml`
2. If cron ≠ `'19 * * * *'` → change to `'19 * * * *'`
3. Stage, commit, push: `git push origin main`

### Push to xystrn
1. Check cron in `.github/workflows/auto-boost.yml`
2. If cron ≠ `'49 * * * *'` → change to `'49 * * * *'`
3. Stage, commit, push: `git push xystrn main --force`

### Push both (default)
When user says "push" without specifying account:
1. Execute shamizen workflow first
2. Execute xystrn workflow second

## Rules

- Check cron before every push
- Only modify cron if value doesn't match target account
- Use strReplace tool for editing (never sed/awk)
- No need to restore cron after push - next push will set correct value

## strReplace Format

```
path: .github/workflows/auto-boost.yml

To 19: oldStr: "    - cron: '49 * * * *'"  newStr: "    - cron: '19 * * * *'"
To 49: oldStr: "    - cron: '19 * * * *'"  newStr: "    - cron: '49 * * * *'"
```
