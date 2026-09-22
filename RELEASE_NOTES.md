# v0.2.0a1 — Local analysis Alpha

The first public distribution of Pallas's local analysis workflow for macOS + Python 3.12–3.13 + Codex / Claude Code.

- Core installation is independent of optional Google application configuration and Meta certificate setup.
- CSV/XLSX campaign/day imports preview and confirm interpretation before retention; duplicate imports are idempotent.
- Meta, Google and TikTok file snapshots use the same analysis template and descriptive calculations.
- Reports preserve missing values, provenance and claim limits. Short date-axis labels avoid overlap.
- Bundled Skills and samples support a first report without advertising credentials; skill updates retain backups.

Validation: 801 automated tests passed; isolated installation, installed CLI/MCP checks, three synthetic media inputs under both generated client configurations, artifact hashes and a browser report check passed. New external users' live authorization, real data reconciliation and natural-language agent adherence remain separate tests.

For a new installation, follow [INSTALL.md](INSTALL.md) and use `npx pallas-ads install`. The original archive `pallas-0.2.0a1-local-alpha.zip` and its checksum remain available in this release. Do not use the automatically generated Source code archives as installers. The full development repository remains private; the distributed wheel contains readable Python runtime code under Apache-2.0.

Not included: hosted ChatGPT access, arbitrary spreadsheet interpretation, cross-file/media merging, ad writes or unattended account management. Default file analysis needs no OpenAI runtime key. Optional media access is subject to the [media authorization guide](AUTHORIZATION.md).

Product: [pallas-ads.com](https://pallas-ads.com/). Support: [support@pallas-ads.com](mailto:support@pallas-ads.com).
