# Customer finder reports

GitHub Actions saves a dated report here every Monday (for whencemedia.com), and whenever you run **Actions > Find customers > Run workflow** with another product URL.

Before it can run, add ONE of these in **Settings > Secrets and variables > Actions**:

- `ANTHROPIC_API_KEY`: from console.anthropic.com (pay per use), or
- `CLAUDE_CODE_OAUTH_TOKEN`: uses your Claude Pro or Max plan.

It never contacts anyone. Reports are a shortlist for you to review.
