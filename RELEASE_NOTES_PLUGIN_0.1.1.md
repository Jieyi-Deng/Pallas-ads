# Pallas native plugin 0.1.1

Clarifies how the shared analysis Skill explains campaign contributions to account CPC changes.
A campaign's weighted contribution is distinct from its own before/after CPC. The Skill also
separates click-share changes from budget history and explains when a short file cannot support
the daily anomaly screen. Runtime calculations and the shared report template are unchanged.

Claude Code 2.1.278 acceptance on macOS completed on 2026-09-22:

- The public 0.1.0 installation loaded three Skills and ten tools, previewed a synthetic Meta
  CSV, waited for confirmation, performed an idempotent import, and generated a qualified report.
- A fresh project and conversation using the 0.1.1 candidate completed first import and report
  generation after confirmation, with correct campaign-contribution interpretation.
- Independently verified spend of USD 368, 16,000 impressions, 240 all-clicks, derived ratios,
  comparison-window CPC, and all ten report artifact hashes in each run.
- Both native manifests, Skill validation, eleven native-plugin Python checks and three built
  distribution integrity checks passed.

The fixture was synthetic. Fresh real-user media authorization, live account reads and unattended
schedules remain separate acceptance work. The unchanged Python runtime is 0.2.0a1; no npm
republish is required. Follow [PLUGIN_INSTALL.md](PLUGIN_INSTALL.md) to update the plugin and
rerun project setup, then start a new host conversation to load the updated Skill.
