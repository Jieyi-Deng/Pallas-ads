<p align="center">
  <a href="https://pallas-ads.com/"><img src="https://raw.githubusercontent.com/Jieyi-Deng/Pallas-ads/main/assets/pallas-logo.png" width="96" height="96" alt="Pallas logo"></a>
</p>

# Pallas

**Advertising analysis, inside your agent.**

**English** | [简体中文](README.zh-CN.md) · [Website](https://pallas-ads.com/) · [npm](https://www.npmjs.com/package/pallas-ads)

Pallas brings advertising data analysis to Codex and Claude Code. Connect an available Meta, Google Ads, or TikTok Ads account, or provide an advertising export, and ask questions in natural language. Pallas checks the data, calculates performance metrics, and produces reports with evidence you can trace back to the source.

Visit **[pallas-ads.com](https://pallas-ads.com/)** to explore the product and its approach to advertising analysis.

## From data to decisions

- **Understand performance.** Review spend, impressions, clicks, and efficiency metrics with clear account and date context.
- **Explain changes.** Explore campaign mix and the arithmetic drivers of metric changes, with business explanations identified as hypotheses when evidence is missing.
- **Get a report you can revisit.** Each report brings together an account and period summary, a breakdown of changes, and findings with recommended next steps.
- **Keep the conversation in your agent.** The `pallas-workflow` and `pallas-analysis` Skills guide the same analysis process across supported data sources.

## 1. Install

You need **macOS, Node.js 22 or later, and Codex or Claude Code** with plugin support.

Ask your agent:

> Install the Pallas plugin from https://github.com/Jieyi-Deng/Pallas-ads using PLUGIN_INSTALL.md, then use its setup Skill to prepare this project.

Or add the source and install directly:

**Codex terminal**

```sh
codex plugin marketplace add Jieyi-Deng/Pallas-ads
codex plugin add pallas@pallas-ads
```

**Claude Code**

```text
/plugin marketplace add Jieyi-Deng/Pallas-ads
/plugin install pallas@pallas-ads
```

See the [plugin guide](PLUGIN_INSTALL.md) for installation and migration. The [npm installer](INSTALL.md), `npx pallas-ads install`, remains available for projects using the project-based installation.

## 2. Activate in your agent

Open your intended project and ask the `pallas-setup` Skill to prepare it. Confirm project trust and any requested permissions, then reload or start a new task.

> Prepare Pallas in this project and verify that its tools and setup, workflow, and analysis Skills are available. Then help me prepare the media account connection I want to use.

Setup prepares the runtime and binds Pallas to your project. Media account authorization is a separate step below.

## 3. Authorize a media account

Ask your agent to connect the platform you want to analyze:

> Help me connect my Meta / Google Ads / TikTok Ads account to Pallas. Check the connection setup for this agent, guide me through browser authorization, and list the accounts I can access. Let me choose the account before reading its performance data.

For a configured connection, complete the platform's sign-in and consent screens, then return to your agent and select the account. If connection setup or account access is needed, follow the [media authorization guide](AUTHORIZATION.md) or contact [support@pallas-ads.com](mailto:support@pallas-ads.com).

If you only want to analyze an uploaded export, skip account authorization and use the file option in the next step.

## 4. Analyze your data

Choose a connected advertising account or upload an advertising export.

### Read a connected account

> Use Pallas to read performance data from my authorized advertising account for the last seven complete days. Confirm the account, reporting dates, currency, timezone, and available data. Analyze performance and changes, explain the evidence behind your findings, and generate an HTML report with recommended next steps.

Your agent retrieves data through the configured media connection and explains its coverage before drawing conclusions. You can continue asking questions about the account and report in the same conversation.

### Upload an advertising export

Attach your CSV or XLSX export if your agent supports local file attachments, or provide its local file path:

> Use Pallas to analyze my uploaded advertising export. First show me the account, date range, field mappings, currency, timezone, and missing data. After I confirm, import it and generate a report covering performance, changes, and recommended next steps. Link the HTML report when it is ready.

Pallas previews the interpretation before saving the import. You confirm what the data represents, and your agent returns the report and explains the findings. See [preparing an advertising export](FILE_IMPORT.md).

## 5. Set up recurring checks

After a successful analysis, use your agent's scheduling feature, where available, to repeat the workflow in the same Pallas project:

> Help me set up a daily check at 9:00 a.m. in my timezone for the advertising account we just analyzed. Confirm the timezone, account, reporting period, and notification preferences with me. On each run, use Pallas to read fresh data, summarize performance changes, and save a report. Report authorization or data retrieval failures explicitly.

The agent manages the schedule; Pallas performs the analysis. Confirm that scheduled runs can access the project, runtime, and authorized connection, and keep the required machine or execution environment available. For file-based checks, supply an updated export before each run: rereading a saved file does not fetch new account data.

## Keep Pallas up to date

Update through your agent's plugin manager, then rerun the setup Skill for each Pallas project and start a new task. See [plugin updates and recovery](PLUGIN_INSTALL.md#update).

For projects still using the npm installation, use the [npm update command](NPM_INSTALLER.md). See [Releases](https://github.com/Jieyi-Deng/Pallas-ads/releases) for change history.

## Your data

Pallas stores imported evidence and reports in your local workspace and has no telemetry. Your chosen agent processes tool results under its own data policy; connected media requests go to the respective platforms. Pallas analyzes performance without changing your advertising campaigns.

## Support

For questions, connection setup, or other needs, contact **[support@pallas-ads.com](mailto:support@pallas-ads.com)**. Use the [feedback guide](NEW_MACHINE_TESTING.md) when sharing a reproducible issue.

[License](LICENSE) · [Notice](NOTICE) · [Trademarks](TRADEMARKS.md)
