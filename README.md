<p align="center">
  <a href="https://pallas-ads.com/"><img src="https://raw.githubusercontent.com/Jieyi-Deng/Pallas-ads/main/assets/pallas-logo.png" width="96" height="96" alt="Pallas logo"></a>
</p>

# Pallas

**Advertising analysis, inside your agent.**

**English** | [简体中文](README.zh-CN.md) · [Website](https://pallas-ads.com/) · [npm](https://www.npmjs.com/package/pallas-ads)

Pallas brings advertising data analysis to Codex and Claude Code. Work with your Meta, Google Ads, and TikTok Ads exports, or connect an available media account, and ask questions in natural language. Pallas checks the data, calculates performance metrics, and produces reports with evidence you can trace back to the source.

Visit **[pallas-ads.com](https://pallas-ads.com/)** to explore the product and its approach to advertising analysis.

## From data to decisions

- **Understand performance.** Review spend, impressions, clicks, and efficiency metrics with clear account and date context.
- **Explain changes.** Explore campaign mix and the arithmetic drivers of metric changes, with business explanations identified as hypotheses when evidence is missing.
- **Get a report you can revisit.** Each report brings together an account and period summary, a breakdown of changes, and findings with recommended next steps.
- **Keep the conversation in your agent.** The `pallas-workflow` and `pallas-analysis` Skills guide the same analysis process across supported data sources.

## 1. Install

You need **macOS, Node.js 22 or later, and Codex or Claude Code**. Run:

```sh
npx pallas-ads install
```

Choose your agent and a new project folder. Pallas sets up its runtime, MCP connection, and analysis Skills; Python is prepared automatically when needed.

You can also ask your agent to install it:

> Install Pallas for my current agent using https://github.com/Jieyi-Deng/Pallas-ads/blob/main/INSTALL.md. Create a new Pallas project, check the installation, and tell me which folder to open to activate it.

See the [installation guide](INSTALL.md) for client-specific commands.

## 2. Activate in your agent

Open the folder printed by the installer in Codex or Claude Code. Confirm project trust and any requested MCP permissions, then start a new task so Pallas tools and Skills can load.

> Check that Pallas and its workflow and analysis Skills are available in this project. Tell me whether I can start analyzing my advertising data.

Activation means loading Pallas in your agent. Media account authorization is a separate step below.

## 3. Analyze your data

Give your agent the local path to a CSV or XLSX export from your advertising platform:

> Use Pallas to analyze my advertising export at /path/to/my-ad-export.csv. First show me the account, date range, field mappings, currency, timezone, and missing data. After I confirm, import it and generate a report covering performance, changes, and recommended next steps. Link the HTML report when it is ready.

Pallas previews the interpretation before saving the import. You confirm what the data represents, and your agent returns the report and explains the findings. See [preparing an advertising export](FILE_IMPORT.md).

## 4. Authorize a media account

For live account data, ask your agent:

> Help me connect my Meta / Google Ads / TikTok Ads account to Pallas. Check the connection setup for this agent, guide me through browser authorization, and list the accounts I can access. Let me choose the account and reporting period before reading its performance data.

For a configured connection, complete the platform's sign-in and consent screens, return to your agent, and select the account to analyze. If connection setup or account access is needed, follow the [media authorization guide](AUTHORIZATION.md) or contact [support@pallas-ads.com](mailto:support@pallas-ads.com). File analysis can be used independently of account authorization.

## Keep Pallas up to date

```sh
npx pallas-ads@latest update --directory /path/to/your-pallas-project
```

Restart your agent task after updating. See [installer commands](NPM_INSTALLER.md) for diagnostics and maintenance, and [Releases](https://github.com/Jieyi-Deng/Pallas-ads/releases) for change history.

## Your data

Pallas stores imported evidence and reports in your local workspace and has no telemetry. Your chosen agent processes tool results under its own data policy; connected media requests go to the respective platforms. Pallas analyzes performance without changing your advertising campaigns.

## Support

For questions, connection setup, or other needs, contact **[support@pallas-ads.com](mailto:support@pallas-ads.com)**. Use the [feedback guide](NEW_MACHINE_TESTING.md) when sharing a reproducible issue.

[License](LICENSE) · [Notice](NOTICE) · [Trademarks](TRADEMARKS.md)
