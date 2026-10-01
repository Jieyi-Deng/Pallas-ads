# Release maintenance

Updated: 2026-10-01 PDT (America/Los_Angeles).

This repository distributes reviewed Pallas artifacts and user documentation.
Product changes, including shared Skills and templates, originate in the upstream
source project. Do not independently patch a shipped Skill or wheel here.

## Release order

1. Merge the upstream implementation PR, including component versions and relevant
   local validation.
2. Prepare and verify one frozen candidate. Keep the runtime, npm installer, plugin
   and renderer versions independent; reuse unchanged published artifacts exactly.
3. Synchronize the selected public files into a branch and open a PR against `main`.
   Review `release.json`, user instructions and applicable checks before merging.
4. Create a GitHub Release from that exact merge commit with a unique release tag.
   Attach its `release.json` and the reviewed npm tgz named in that manifest.
5. Publish the same tgz to npm. Verify an anonymous registry download, integrity and
   the `latest` tag, then update the release notes with the actual channel status.

`release.json` describes the product artifacts in this checkout. Publisher tooling
is tracked separately in the upstream frozen candidate and verified against public
main before publication; tooling-only edits do not change product metadata. It is not proof of npm
publication. Consult the [npm package](https://www.npmjs.com/package/pallas-ads)
and [GitHub releases](https://github.com/Jieyi-Deng/Pallas-ads/releases) for channel
availability. Ordinary documentation and publisher-tool changes do not by themselves
require a new product package or release tag.

Never reuse a package version for different bytes or move an existing release tag.
A GitHub release may precede npm availability; say so until registry verification
succeeds. A failed or interrupted publication should be inspected before retrying.

## Local publication checks

The reviewed candidate contains the dedicated npm README and tgz. Do not run
`npm pack` in this checkout to recreate that artifact: the root README serves a
different purpose and would change its integrity.

```sh
python tools/npm_publish.py --manifest /path/to/release.json --archive /path/to/pallas-ads-VERSION.tgz
python tools/npm_publish.py --manifest /path/to/release.json --archive /path/to/pallas-ads-VERSION.tgz --publish
```

The publisher verifies the package allowlist, nested wheel exclusions, file hashes
and manifest identity. It checks the registry first: an existing identical package
already tagged `latest` is a successful no-op; a version collision is an error.
Moving `latest` to an existing or older version requires an explicit `--promote`
and a deliberate maintainer decision. Registry processing is exit code 75; check
again before reporting completion. Upstream's release CLI additionally requires
local candidate verification and matching artifacts merged into public `main`.

## Actions and optional trusted publishing

Local checks come first. Product PRs run one Linux distribution job. Publisher-only
PRs run the small offline publisher suite. Root/docs Markdown changes run neither.
Shared Skill Markdown remains behavior and requires distribution checks. Hosted
macOS verification is an explicit manual option when local verification is insufficient.

The manual `npm-publish.yml` workflow is initially disabled by its repository-variable
gate. It downloads an existing reviewed GitHub Release tgz, verifies the release
manifest against its tag, and publishes without rebuilding or rerunning product tests.
It requires all of the following owner configuration:

- npm trusted publisher for repository `Jieyi-Deng/Pallas-ads`, workflow
  `npm-publish.yml`, environment `npm-release`, with direct publishing allowed.
- Appropriate protections for the GitHub `npm-release` environment.
- Repository variable `NPM_TRUSTED_PUBLISHING_ENABLED=true`.
- Manual dispatch from `main`, a published release tag, and `confirm_publish=true`.

Account binding and enabling this gate are separate owner actions. Until configured,
use the local publisher with npm's normal authentication. Existing release tags that
predate `release.json` and the npm tgz assets cannot use this workflow; do not modify
those historical tags to retrofit it.

See [npm trusted publishing](https://docs.npmjs.com/trusted-publishers/) for account
requirements. The workflow does not establish host-model, live-account or external-user
acceptance. Keep evidence levels and known data limitations explicit in release notes.
