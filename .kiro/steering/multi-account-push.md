---
inclusion: auto
---

# Multi-Account Push Strategy

This repository pushes to two GitHub accounts with different cron schedules.

## Accounts

1. **shamizen** (origin) - Cron: `'19 * * * *'`
2. **xystrn** (secondary) - Cron: `'49 * * * *'`

## Push Commands

### Push to xystrn

**Trigger:** "push to xystrn" or "push xystrn"

**Steps:**
1. Use `strReplace` on `.github/workflows/auto-boost.yml`:
   - oldStr: `cron: '19 * * * *'`
   - newStr: `cron: '49 * * * *'`
2. Commit: "Update cron for xystrn"
3. Push to xystrn remote
4. Use `strReplace` to restore:
   - oldStr: `cron: '49 * * * *'`
   - newStr: `cron: '19 * * * *'`
5. Commit: "Restore cron to 19"

### Push to shamizen

**Trigger:** "push to shamizen", "push shamizen", "push to origin"

**Steps:**
1. Verify cron is `'19 * * * *'` in `.github/workflows/auto-boost.yml`
2. Push to origin remote

## Important

- Use `strReplace` tool, NOT sed or command line text editing
- Local repo always keeps cron at `'19 * * * *'`
- Only temporarily change to `'49 * * * *'` when pushing to xystrn
