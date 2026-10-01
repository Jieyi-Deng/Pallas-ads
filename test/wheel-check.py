"""Verify that both distribution channels ship the same complete, reviewed runtime."""

import hashlib
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugin = root / "plugins/pallas"
manifests = [json.loads((path / "resources/npm-runtime.json").read_text()) for path in (root, plugin)]
assert manifests[0] == manifests[1], "Installer/plugin runtime manifests differ"
manifest = manifests[0]
for path in (root, plugin):
    for name, expected in manifest["files"].items():
        assert Path(name).name == name, "Runtime manifest paths must be flat"
        actual = hashlib.sha256((path / "resources" / name).read_bytes()).hexdigest()
        assert actual == expected, f"Runtime checksum mismatch: {path.name}/{name}"

with zipfile.ZipFile(root / "resources" / manifest["wheel"]) as wheel:
    names = wheel.namelist()
    forbidden = {"PALLAS_HANDOFF.md", "PALLAS_PRODUCT.md", "PALLAS_PROJECT.md", "AGENTS.md", "google-desktop.json"}
    assert not any(forbidden.intersection(Path(name).parts) for name in names)
    assert not any(part in {".env", ".pallas", "local_docs", "__pycache__"} for name in names for part in Path(name).parts)
    for module in ("command", "command_cli", "dashboard", "dashboard_import", "dashboard_tools", "competitor_report", "internal_conversions"):
        assert f"pallas_ads/{module}.py" in names, f"Missing runtime module: {module}"
    for skill in ("pallas", "pallas-analysis", "pallas-workflow", "pallas-dashboard", "pallas-competitors"):
        for file in (plugin / "skills" / skill).rglob("*"):
            if file.is_file():
                member = "pallas_ads/resources/" + str(file.relative_to(plugin))
                assert wheel.read(member) == file.read_bytes(), f"Skill/wheel mismatch: {member}"
    status = json.loads(wheel.read("pallas_ads/resources/release-status.json"))
    package = json.loads((root / "package.json").read_text())
    assert package["version"].replace("-alpha.", "a") == status["package_version"]
    assert not status["advertising_writes"] and not status["default_telemetry"]

print("Installer/plugin checksums, runtime modules, Skill identity and private-file exclusions passed.")
