# Pallas releases

## Current distribution

The current published distribution is [release-20261012-01](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/release-20261012-01):

| Component | Version |
| --- | --- |
| Native plugin | 0.2.6 |
| Python runtime | 0.2.0a8 |
| npm installer | 0.2.0-alpha.8 |
| Analysis renderer | 2.5.0 |
| Dashboard renderer | 2.2.2 |
| Competitor renderer | 2.1.0 |

On October 18, 2026 (PDT), npm version `0.2.0-alpha.8` was verified as published and tagged `latest`. This is a dated observation: consult [npm](https://www.npmjs.com/package/pallas-ads) for current registry availability and [release.json](release.json) for this checkout's component versions. Channels can update at different times.

This release adds Windows 11 x64 installation and runtime support as an Alpha preview, retains macOS compatibility and report-language support, and fixes the dashboard header layout. Windows 11 real-machine acceptance remains pending. Update through the [plugin manager](PLUGIN_INSTALL.md#update) or [npm installer](NPM_INSTALLER.md#update), rerun project setup where applicable, and start a new agent task.

This is an engineering Alpha. Pallas-owned Meta login does not yet enable account discovery or reporting. Google production-data validation and complete Meta reconciliation remain outstanding. Installed synthetic tests and maintainer distribution checks do not establish independent external-user or live-account acceptance. See [authorization limits](AUTHORIZATION.md) and each release's validation record.

## Release history

GitHub Release records are the canonical historical notes; versions, validation, and limitations in those records describe that release, not the current distribution.

| Release | Main change |
| --- | --- |
| [release-20261012-01](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/release-20261012-01) | Windows 11 x64 Alpha preview and dashboard header layout fix; runtime a8, plugin 0.2.6, npm alpha.8 |
| [release-20261006-01](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/release-20261006-01) | Shared report-language rules; runtime a6, plugin 0.2.4, npm alpha.6 |
| [release-20261005-02](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/release-20261005-02) | Publisher-configured browser authorization; runtime a5, plugin 0.2.3, npm alpha.5 |
| [release-20261005-01](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/release-20261005-01) | Authorization diagnostics and recovery; runtime a4, plugin 0.2.2, npm alpha.4 |
| [release-20261003-01](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/release-20261003-01) | Report, competitor, and dashboard updates; runtime a3, plugin 0.2.1, npm alpha.3 |
| [plugin-v0.2.0](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/plugin-v0.2.0) | Unified command, persistent dashboards, and companion Skills; runtime a2, npm alpha.2 |
| [plugin-v0.1.1](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/plugin-v0.1.1) | Campaign-contribution interpretation |
| [plugin-v0.1.0](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/plugin-v0.1.0) | Initial native plugin |
| [npm-v0.2.0-alpha.1](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/npm-v0.2.0-alpha.1) | Initial npm installer |
| [v0.2.0a1](https://github.com/Jieyi-Deng/Pallas-ads/releases/tag/v0.2.0a1) | Historical local-analysis ZIP |

The original ZIP and checksum remain attached to the historical a1 release. Recent releases attach the reviewed npm tgz and release manifest. Do not use GitHub-generated source archives as installers.
