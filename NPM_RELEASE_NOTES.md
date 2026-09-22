# npm installer 0.2.0-alpha.1

One-command installation for macOS Apple Silicon and Intel, using Node.js 22+.

- Interactive Codex/Claude selection and new-project path; explicit flags for agent automation.
- Reuse supported Python or provision a private Python 3.13 environment with pinned, hash-verified uv.
- Install runtime 0.2.0a1, MCP configuration, both Skills and synthetic examples.
- Doctor, idempotent reinstall detection and update with Skills backup; preserve local data.
- No media login, certificate changes or runtime API key in default setup.

Seven launcher unit tests and 22 Python setup regressions passed. Existing-Python Claude and managed-Python Codex installations produced reports through installed MCP, with 12 separate process operations per project. Update preserved synthetic data and backed up custom Skills. macOS managed Python uses venv symlinks to retain dylib resolution.

This npm installer version wraps the unchanged reviewed Python wheel 0.2.0a1. Original ZIP assets are retained unchanged. The `.tgz` is an npm package, not a source repository export. Full source remains private; distributed runtime code remains readable and Apache-2.0 licensed.

At preparation time npm registry publication required publisher 2FA; the GitHub package command is independent of npm registry publishing. Consult the main README for the current short-command availability.
