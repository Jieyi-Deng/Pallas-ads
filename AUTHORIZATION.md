# Connect an advertising account

Complete [plugin installation and activation](PLUGIN_INSTALL.md) or the [npm installation](INSTALL.md)
first. Installation alone does not grant media access. File analysis needs no media authorization.

## Start in your agent

> Connect my Google Ads / Meta Ads / TikTok Ads account to Pallas. Open browser login, wait for the
> authorization result, and explain whether account discovery is available for this connection.

Pallas checks the selected platform, opens your system browser and waits for the result. Sign in
and review consent yourself, including any MFA. Return to the same chat afterward. You do not
need to create a developer app, import JSON, configure a certificate or paste tokens into chat.

If the browser cannot open automatically, the agent supplies a clickable login link for the
pending session. If you cancel, wait too long or close the agent session, ask to start login again.
An explicit request to sign in again creates a new session even when an earlier connection exists.
The old Pallas grant is retained until its replacement succeeds.

## Choose a connection route

| Platform, both Codex and Claude Code | Publisher-configured release | After consent |
|---|---|---|
| Google Ads | Bundled Google Desktop application, browser consent and local callback | Discover accounts, select one, then choose a reporting period. Cloud project access and your account permissions still apply. |
| Meta Ads | Pallas's public application, browser consent and Pallas HTTPS callback returning to the local app | Pallas-owned authorization is implemented; its Meta data adapter remains pending. Login alone does not enable account discovery or reports. |
| TikTok Ads | Pallas uses the official TikTok MCP browser flow | Discover accounts, select one and inspect available data. Live metric reconciliation remains separate. |

The new Google/Meta flow requires a publisher-configured release and completed platform setup.
Older core releases, including npm alpha.4 / plugin 0.2.2, do not include those applications.
If setup is missing, the publisher supplies the corrected release; advertisers do not configure
client IDs or files. Platform verification, application eligibility and fresh external-user
acceptance are separate from local software tests. Access is not guaranteed for every account.

Google's callback stays on your computer. Meta sends a short-lived authorization code and random
state through `https://pallas-ads.com/oauth/meta/callback`, hosted on Cloudflare Pages, before the
browser forwards them to a temporary local receiver. The page has no analytics or token storage.
Token exchange happens locally with PKCE; Pallas tokens use the operating system credential store.
See the [privacy policy](https://pallas-ads.com/privacy) for data flow and hosting information.

## Enable Meta in Claude Code

This section applies only to an existing **host-managed** `meta_official` connection. Its login
belongs to Claude Code and is independent of Pallas-owned authorization. The setup Skill can
retain/register this legacy route and its read-tool guard. Interactive Claude Code terminals
can use `/mcp`; the desktop Code tab does not provide that command. Prefer the publisher-configured
Pallas flow for new browser-login installations. No tokens are copied between the two routes.

Existing Codex host-managed Meta connections also remain separate. A successful read through
another installed Meta connector is not evidence that Pallas's new connection is authorized.

Review the actual consent screen. The official Meta MCP requires `ads_read` and
`ads_mcp_management`; a successful consent does not permit Pallas to modify campaigns or budgets.
Do not disable read-tool guards to work around failures.

## Credentials and disconnection

Complete passwords, consent and MFA on the platform. Never paste passwords, tokens, browser
cookies or client configuration into chat or public issues. Ask Pallas to disconnect its own
connection; use host controls for host-managed connections. Revoke remote access separately in
the media platform. Removing a workspace alone does not revoke consent.

For help, contact [support@pallas-ads.com](mailto:support@pallas-ads.com) with your agent/version,
platform, failed step and sanitized error. You can use [advertising exports](FILE_IMPORT.md)
while platform access is being resolved.
