# Verify your setup and share feedback

Use this guide after [installing and activating Pallas](INSTALL.md). It helps you check the experience with your own advertising data and provide useful feedback.

## Check activation

Open the generated project in Codex or Claude Code, confirm project trust, and start a new task. Ask the agent to verify that Pallas tools, `pallas-workflow`, and `pallas-analysis` are available.

Run installation diagnostics if needed:

```sh
npx pallas-ads doctor --directory /path/to/your-pallas-project
```

Optional media setup messages do not prevent file analysis. The diagnostic does not replace checking actual tool loading in the agent.

## Generate a report

Provide a CSV or XLSX export prepared according to [FILE_IMPORT.md](FILE_IMPORT.md):

> Analyze this advertising export with Pallas. Show me the interpretation before importing it. After I confirm, generate a report covering account performance, changes, and recommended next steps. Explain missing data and distinguish measured findings from business hypotheses.

Review the following with your agent:

| Check | Expected behavior |
|---|---|
| Interpretation | Account, dates, mappings, currency, timezone, and missing values match the export. |
| Confirmation | You confirm the interpretation in ordinary language without entering hashes, dataset IDs, or JSON. |
| Data issues | Invalid dates, formulas, totals, or duplicate campaign/day rows produce a specific explanation. |
| Calculations | CTR uses total clicks / total impressions; CPC uses spend / clicks; CPM uses spend / impressions × 1,000. Missing values remain unknown. |
| Reasoning | Metric changes and campaign mix are explained with evidence. Unverified business causes are identified as hypotheses. |
| Report | The HTML opens, units are clear, and the conversation matches the report. |
| Repeat use | Re-importing the same data does not double-count it, and retained datasets remain available after restarting. |
| Live data, if connected | The authorized account, period, currency, and totals are checked against the media platform. |

For live account setup, use [AUTHORIZATION.md](AUTHORIZATION.md). Record authorization, account discovery, data retrieval, and report reconciliation separately. Mark any step you did not perform as `not_run`.

## Describe a problem

Send [support@pallas-ads.com](mailto:support@pallas-ads.com) a short description with:

- Your operating system and agent.
- The installer/runtime versions from diagnostics, for troubleshooting.
- The operation, expected result, and actual result.
- The exact sanitized error and any retries.
- The extra manual steps you had to take.

You can also open a GitHub issue with a sanitized reproduction. Do not attach tokens, raw account exports, account identifiers, or private reports to a public issue. Version identifiers belong in diagnostics and feedback, not in the product introduction.

## Prepare a feedback bundle

If support requests a structured bundle, ask your agent to use the installed runtime's `pallas` CLI:

1. Run `pallas acceptance start --directory /path/to/unique-feedback-run`.
2. Record the review in `share/SUMMARY.md`; leave untested entries in `results.json` as `not_run`.
3. Keep original reports local and index them in `LOCAL_REPORT_INDEX.md`.
4. Prepare sanitized report copies with the attachments needed to inspect them, then show you the proposed shared files.
5. After your review, run `pallas acceptance pack --directory /path/to/unique-feedback-run --reviewed`.

Packaging creates a local archive; it does not send it. You decide whether to email the reviewed bundle.

## Update or remove Pallas

Follow [NPM_INSTALLER.md](NPM_INSTALLER.md) for updates, interrupted installations, and removal. Back up your project first. Keep `.pallas` if you want to retain imported data and reports, and revoke media authorization separately when needed.
