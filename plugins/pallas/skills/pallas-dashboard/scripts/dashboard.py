"""Run with the installed Pallas Python environment; all logic lives in the runtime."""

try:
    from pallas_ads.dashboard_tools import main
except ImportError:
    raise SystemExit(
        "This Pallas runtime lacks dashboard helpers. Use pallas-setup to align the runtime "
        "and skill versions; do not replace the helper with ad hoc processing code."
    ) from None

if __name__ == "__main__":
    main()
