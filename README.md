# Pallas Ads

[简体中文](README.zh-CN.md) · **Local analysis Alpha 0.2.0a1**

Analyze advertising data in your own Codex or Claude Code. Pallas checks data, calculates metrics and generates local reports; your agent handles the conversation and reasoning.

This is the **public distribution repository**. The full development repository remains private. The downloadable Python wheel includes readable runtime code, the two Pallas Skills and report templates; it is not a binary-only or source-hidden package. Distributed Pallas material retains its Apache-2.0 license.

## Install through your agent

A local installation is necessary, but your agent can perform it. Give Codex or Claude Code this request:

> Install Pallas for my current agent by following https://github.com/Jieyi-Deng/Pallas-ads/blob/v0.2.0a1/INSTALL.md . Use the default local analysis mode in a new project. Download and verify the release, install it, then tell me which project to open and start a new task in. Do not enable live media connections yet.

Requirements: **macOS, Python 3.12 or 3.13, Codex or Claude Code**, and internet access to download dependencies. The installer creates a separate runtime and project; it does not replace global agent settings or existing projects. The agent may need your approval for installation and project trust. No extra OpenAI runtime API key, Meta certificate or Google developer file is required for default local analysis.

[Installation instructions](INSTALL.md) · [Download v0.2.0a1](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/v0.2.0a1) · [Test guide](NEW_MACHINE_TESTING.md)

Download the attached `pallas-0.2.0a1-local-alpha.zip`, not GitHub's automatically generated “Source code” archive, which contains only this distribution repository's documents.

## First report

After installation, open the generated project in your agent, trust it and start a new task. Ask:

> Use Pallas to analyze samples/meta_campaign_daily.csv. Preview the account, period, field mappings, currency, timezone and missing values. After I confirm that interpretation, import it and generate the three-part HTML report. Distinguish observations, arithmetic contributions and unverified business explanations. This is synthetic data; do not connect a live account.

Google and TikTok synthetic samples are also included. Your own exports must follow the [supported CSV/XLSX format](FILE_IMPORT.md): one platform/account/currency, daily campaign rows, no duplicate campaign-day rows or formulas. Multiple files are independent snapshots, not an automatic combined report.

## What this release establishes

- Preview → confirmation → local import → shared HTML report.
- Aggregated spend, impressions, clicks, CTR/CPC/CPM, arithmetic change contributions and campaign mix.
- Missing values and zero denominators remain unknown; business causes and conversion semantics are not invented.
- Repeated imports reuse the same snapshot; retained data works after process restart.
- 801 automated regression tests passed. An isolated installation and both generated client configurations were exercised through stdio MCP with synthetic data. These checks do not certify human-agent adherence or real account reconciliation.

Live connections are optional and experimental. Google live access requires maintainer-provided application configuration and platform eligibility. Meta/Claude uses the host's official MCP; Meta/Codex uses an explicitly configured internal preregistered route. Public, invitation-free Meta access for every new user is not established. TikTok account eligibility also needs real testing. See the [live media matrix](NEW_MACHINE_TESTING.md#可选实时连接).

This Alpha does not include a hosted ChatGPT service, cross-file/media aggregation or unattended account management. It does not modify ad campaigns.

## Data and feedback

Pallas has no telemetry and stores evidence locally. Your chosen agent receives tool results and applies its own data policy. Optional media requests go to the relevant platform. Never publish credentials, raw account exports or private report attachments in an issue. Follow the test guide to review sanitized feedback before sharing; packing a feedback archive does not upload it.

Report reproducible, sanitized problems in this repository's Issues. This is an individual portfolio project with no paid service in this release. Pallas is not endorsed by the media or agent providers.

[License](LICENSE) · [Notice](NOTICE) · [Trademarks](TRADEMARKS.md)
