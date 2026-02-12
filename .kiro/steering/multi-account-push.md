---
inclusion: auto
---

# Multi-Account Push Strategy

**IMPORTANT: When user says "push" or "save and push" → ALWAYS push to BOTH accounts automatically**

This repository syncs to two GitHub accounts with different cron schedules.

## Account Mapping

- **shamizen** (origin remote) → cron: `'19 * * * *'`
- **xystrn** (xystrn remote) → cron: `'49 * * * *'`

## Default Behavior: Push to BOTH Accounts

When user says "push", "save and push", or "push to github" without specifying account:

1. **Push to shamizen first:**
   - Check cron in `.github/workflows/auto-boost.yml`
   - If cron ≠ `'19 * * * *'` → change to `'19 * * * *'`
   - Stage, commit, push: `git push origin main`

2. **Then push to xystrn:**
   - Check cron in `.github/workflows/auto-boost.yml`
   - If cron ≠ `'49 * * * *'` → change to `'49 * * * *'`
   - Stage, commit, push: `git push xystrn main --force`

## Single Account Push (only if explicitly specified)

User must explicitly say "push to shamizen only" or "push to xystrn only"

### Push to shamizen only
1. Check cron in `.github/workflows/auto-boost.yml`
2. If cron ≠ `'19 * * * *'` → change to `'19 * * * *'`
3. Stage, commit, push: `git push origin main`

### Push to xystrn only
1. Check cron in `.github/workflows/auto-boost.yml`
2. If cron ≠ `'49 * * * *'` → change to `'49 * * * *'`
3. Stage, commit, push: `git push xystrn main --force`

## Rules

- **Default = push both accounts** (don't ask, just do it)
- **ALWAYS check and update cron before every push** (for both single and dual account pushes)
- Only modify cron if value doesn't match target account
- Use strReplace tool for editing (never sed/awk)
- No need to restore cron after push - next push will set correct value

## strReplace Format

```
path: .github/workflows/auto-boost.yml

To 19: oldStr: "    - cron: '49 * * * *'"  newStr: "    - cron: '19 * * * *'"
To 49: oldStr: "    - cron: '19 * * * *'"  newStr: "    - cron: '49 * * * *'"
```
