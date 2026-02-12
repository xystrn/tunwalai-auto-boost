# Tunwalai Auto Boost

Automated bot to boost stories on Tunwalai every hour via GitHub Actions (free).

## What does it do?

1. **Click Promote button** - Story appears in "Promoted Stories"
2. **Edit + Save twice** - Story appears in "Latest Updates" feed
3. **Supports multiple stories** - Login once, process all stories

## Setup

### 1. Fork this repo
Click the "Fork" button at the top right

### 2. Configure Secrets
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Go to **Secrets** tab → **New repository secret**
3. Create 2 secrets:
   - `TUNWALAI_USERNAME` = your login email
   - `TUNWALAI_PASSWORD` = your password

### 3. Configure Story IDs
1. Go to **Variables** tab → **New repository variable**
2. Create:
   - Name: `STORY_IDS`
   - Value: your story ID(s)
     - Single story: `838611`
     - Multiple stories: `838611,123456,789012` (comma-separated, no spaces)
     - Supports URLs: `https://www.tunwalai.com/story/838611,https://www.tunwalai.com/story/123456`
     - If not set, defaults to `838611`

**Why use Variable?** So you can see which stories are being processed in the logs (safe for private repos).

### 4. Enable Actions
1. Go to **Actions** tab
2. Click **I understand my workflows, go ahead and enable them**

### 5. Test
1. Go to **Actions** → **Auto Promote & Update**
2. Click **Run workflow** → **Run workflow**
3. Check the logs to verify it works

## Schedule

Default: Runs every hour at minute 19 (00:19, 01:19, 02:19, etc.)

Check `.github/workflows/auto-boost.yml` for the actual schedule configured in your repo.

## Change Schedule

Edit `.github/workflows/auto-boost.yml`:

```yaml
schedule:
  - cron: '19 * * * *'  # Every hour at minute 19
```

Examples:
- Every 2 hours: `'0 */2 * * *'`
- Every 30 minutes: `'*/30 * * * *'`
- Specific times: `'0 9,12,15,18 * * *'` (9am, 12pm, 3pm, 6pm)

**Note**: If you fork this repo multiple times for different accounts, change the cron schedule in each fork to avoid running at the same time (e.g., use minute 19 for account 1, minute 49 for account 2).

## Troubleshooting

**View Logs**: Actions → Click workflow run → promote → Run bot

**Login Failed**: Check username/password in Secrets

**Element Not Found**: Website HTML changed → Update selectors in `bot.py`

**Timeout**: Increase `timeout-minutes` in workflow file if you have many stories

## How It Works

1. **Login once** - Checks if already logged in, otherwise logs in
2. **For each story**:
   - Click Promote button (if available)
   - Edit + Save (round 1)
   - Edit + Save (round 2)
3. **Summary** - Shows success/failure count

## Notes

- Login is shared across all stories (efficient)
- If one story fails, others continue processing
- Random delays (1-4s) make it look natural
- Works in headless Chrome (no GUI needed)
