# Updating Pallas

For product questions or connection setup, contact [support@pallas-ads.com](mailto:support@pallas-ads.com).

## Change workflow

1. Start from the latest `main` and create a branch before editing. Use the `codex/` prefix for agent-created branches.
2. Make and review changes on that branch. Keep the English and Chinese README aligned; other documentation is maintained in English.
3. Run checks appropriate to the change and open a pull request against `main`.
4. Merge the reviewed branch after required checks pass. Do not commit product or documentation updates directly to `main`.

Keep release identifiers and historical validation details in release notes. Product onboarding follows installation, activation, media authorization, analysis (connected accounts or uploaded files), and recurring checks through the user's agent. File-only analysis does not require media authorization.

## Local checks and Actions

Run `node --test test/*.test.mjs` and `python test/wheel-check.py` locally. For a release, install the shipped wheel in a fresh Python 3.12 or 3.13 virtual environment and run `test/command-smoke.py` with `--python`, `--plugin plugins/pallas`, and a new `--output` directory. On macOS, verify native setup, doctor, `test/plugin-smoke.mjs`, and upgrade data preservation locally. These use synthetic data and do not authorize media.

Product PRs run one Linux distribution job, including a clean wheel install and command acceptance. Root documentation-only changes skip Actions; Skills and templates still run checks. Automatic runs are PR-only, and concurrency is scoped to this workflow and PR/ref. Use the explicit `include_macos` manual input only when an additional hosted macOS release check is needed.
