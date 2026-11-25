# First Customer Finder on GitHub

Every Monday at 08:47 IST, GitHub Actions runs this skill with Claude for whencemedia.com. Prospects that have a public business email go into the **India** tab of the Whence Lead Crawler sheet with Status "New". Anyone already in the sheet is skipped. The full report is kept as a download on the run page for 30 days. It is not saved in this repo, because the repo is public.

To run it for another brand, go to **Actions > Find customers > Run workflow** and enter its URL. Untick "Add prospects" if the results are for a client and shouldn't go into Whence's lead sheet.

Secrets, in **Settings > Secrets and variables > Actions**:

- `ANTHROPIC_API_KEY` (pay per use) or `CLAUDE_CODE_OAUTH_TOKEN` (your Claude plan). One of these is required.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: the same Google key used by the Maps scraper. The sheet must be shared with it as an Editor.

It never contacts anyone.
