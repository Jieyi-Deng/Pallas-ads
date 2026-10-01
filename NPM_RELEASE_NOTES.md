# npm installer 0.2.0-alpha.2

The npm and GitHub packages now bundle runtime 0.2.0a2, the unified Pallas command, and five portable Skills. Native plugin 0.2.0 is a separate entrypoint. See [the release notes](RELEASE_NOTES_PLUGIN_0.2.0.md) and [installer reference](NPM_INSTALLER.md) for update commands and validation.

Published to npm on October 1, 2026, as `pallas-ads@0.2.0-alpha.2` with `latest` pointing to this version. Install with `npx pallas-ads install`; update an npm-managed project with `npx pallas-ads@latest update --directory /absolute/path/to/project`. The bundled runtime and launcher are unchanged from the verified GitHub release.

# npm installer 0.2.0-alpha.1

One-command installation for macOS Apple Silicon and Intel, using Node.js 22+.

- Interactive Codex/Claude selection and new-project path; explicit flags for agent automation.
- Reuse supported Python or provision a private Python 3.13 environment with pinned, hash-verified uv.
- Install runtime 0.2.0a1, MCP configuration, both Skills and synthetic examples.
- Doctor, idempotent reinstall detection and update with Skills backup; preserve local data.
- No media login, certificate changes or runtime API key in default setup.

Seven launcher unit tests and 22 Python setup regressions passed. Existing-Python Claude and managed-Python Codex installations produced reports through installed MCP, with 12 separate process operations per project. Update preserved synthetic data and backed up custom Skills. macOS managed Python uses venv symlinks to retain dylib resolution.

This npm installer version wraps the unchanged reviewed Python wheel 0.2.0a1. Original ZIP assets are retained unchanged. The `.tgz` is an npm package, not a source repository export. Full source remains private; distributed runtime code remains readable and Apache-2.0 licensed.

Published on npm as `pallas-ads@0.2.0-alpha.1` with the `latest` tag after publisher security verification. Run `npx pallas-ads install`; no npm account is needed for installation. The GitHub package entry remains available.

Start with [installation and activation](INSTALL.md), then [analyze an export](FILE_IMPORT.md) or [connect a media account](AUTHORIZATION.md). For help, contact [support@pallas-ads.com](mailto:support@pallas-ads.com).
