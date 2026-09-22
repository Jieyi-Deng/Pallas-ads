# Connect an advertising account

Native plugin users: complete [installation and activation](PLUGIN_INSTALL.md) first. Plugin installation does not grant media access. The setup Skill configures Claude Code Meta when requested and preserves existing Codex connections.

Account authorization allows an available media connection to read data you can access. It is separate from installing and activating Pallas. You can analyze a local advertising export without connecting a media account.

## Start in your agent

> Help me connect my Meta / Google Ads / TikTok Ads account to Pallas. Check the connection setup, guide me through browser authorization, and list the accounts I can access. Let me choose the account and reporting period before reading performance data.

1. The agent checks the selected platform's connection setup.
2. For a configured route, open the platform's authorization page.
3. Sign in yourself and review the requested access. Complete any account selection, consent, and MFA shown by the platform.
4. Return to the agent and list accessible advertising accounts. Choose the account and reporting period there; consent screens do not always include account selection.
5. Ask Pallas to retrieve the selected data and explain its coverage before analysis.

Successful sign-in does not by itself establish access to an advertising account. Confirm that the expected account is listed and that the requested reporting period can be read.

## Choose a connection route

| Platform and agent | Connection setup | Next step |
|---|---|---|
| TikTok Ads, Codex or Claude Code | Pallas uses the official TikTok MCP connection. | Ask Pallas to connect TikTok, complete browser consent, and discover available accounts. |
| Meta, Claude Code | Claude Code manages the official Meta MCP connection. The default npm project does not enable it. | Prepare a Meta-enabled project as described below, authenticate `meta_official` through `/mcp`, and list accounts. |
| Meta, Codex | The provided route needs a registered application identity and local HTTPS callback setup. It is not enabled by the npm installer. | Contact [support@pallas-ads.com](mailto:support@pallas-ads.com) for compatible setup and account eligibility before starting authorization. |
| Google Ads, Codex or Claude Code | Pallas uses the Google Ads API. Live access requires configured application identity and platform access; the public core package does not supply them. | Contact [support@pallas-ads.com](mailto:support@pallas-ads.com) for connection setup, then complete Google browser consent and account discovery. |

Access depends on your platform permissions and the configured application's eligibility. If an application requires a test-user invitation, support will confirm the required setup. Do not create your own developer application just to analyze an exported file.

## Enable Meta in Claude Code

An agent can use the runtime from an existing npm installation to create a **separate, new** project with the official Meta connection and Pallas's read-tool guard. For the default Claude installation paths:

```sh
"$HOME/pallas-claude-runtime/bin/pallas" agent setup --client claude --mode live --directory "$HOME/pallas-meta-claude"
```

Adjust the runtime path if the original installation used a different name. Do not run setup over a populated project. The new project shares the original runtime, so keep that runtime in place. It is created by the runtime CLI and has no separate npm installer receipt; use the original npm project when updating the shared runtime, then refresh this project's Skills using that runtime's `agent refresh-skills` command.

Open the new project in Claude Code, confirm trust and the MCP/hook configuration, and start a new task. Open `/mcp`, select `meta_official`, and choose Authenticate. Complete the Meta page and return to Claude Code to discover accounts.

The consent page may request advertising management permissions even though Pallas's project guard restricts analysis to its allowed read tools. Review the actual consent shown. Do not disable that guard to get around a failed request. If authorization or account access fails, retain the error and contact support.

## Credentials and disconnection

Complete passwords, consent, and MFA in the platform's own interface. Do not paste tokens, API keys, passwords, or browser cookies into chat or public issues. Do not transfer authorization tokens between ChatGPT, Codex, and Claude Code.

Disconnect a host-managed connection in the agent that authorized it. Revoke remote consent in the media platform when you want to remove that access. Removing a Pallas workspace alone does not revoke a platform authorization.

## When a connection needs help

Tell [support@pallas-ads.com](mailto:support@pallas-ads.com) which agent and platform you use, which step failed, and the sanitized error. Share an email address for a test invitation only if support confirms it is needed; never share credentials. You can continue using [advertising exports](FILE_IMPORT.md) while connection setup is resolved.
