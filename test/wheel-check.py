"""Verify that both distribution channels ship the same complete, reviewed runtime."""

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
plugin = root / "plugins/pallas"
manifests = [
    json.loads((path / "resources/npm-runtime.json").read_text()) for path in (root, plugin)
]
assert manifests[0] == manifests[1], "Installer/plugin runtime manifests differ"
manifest = manifests[0]
for path in (root, plugin):
    for name, expected in manifest["files"].items():
        assert Path(name).name == name, "Runtime manifest paths must be flat"
        actual = hashlib.sha256((path / "resources" / name).read_bytes()).hexdigest()
        assert actual == expected, f"Runtime checksum mismatch: {path.name}/{name}"

spec = importlib.util.spec_from_file_location(
    "pallas_public_validation", root / "tools/npm_publish.py"
)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
validator.verify_wheel(
    (root / "resources" / manifest["wheel"]).read_bytes(),
    json.loads((root / "resources/release-manifest.json").read_text()),
)

with zipfile.ZipFile(root / "resources" / manifest["wheel"]) as wheel:
    names = wheel.namelist()
    for module in (
        "command",
        "command_cli",
        "dashboard",
        "dashboard_import",
        "dashboard_tools",
        "competitor_report",
        "internal_conversions",
    ):
        assert f"pallas_ads/{module}.py" in names, f"Missing runtime module: {module}"
    for skill in (
        "pallas",
        "pallas-analysis",
        "pallas-workflow",
        "pallas-dashboard",
        "pallas-competitors",
    ):
        for file in (plugin / "skills" / skill).rglob("*"):
            if file.is_file():
                member = "pallas_ads/resources/" + str(file.relative_to(plugin))
                assert wheel.read(member) == file.read_bytes(), f"Skill/wheel mismatch: {member}"
    status = json.loads(wheel.read("pallas_ads/resources/release-status.json"))
    package = json.loads((root / "package.json").read_text())
    assert manifest["runtimeVersion"] == status["package_version"]
    assert not status["advertising_writes"] and not status["default_telemetry"]

release = json.loads((root / "release.json").read_text())
assert release["schema_version"] == 1
assert release["components"]["runtime"] == status["package_version"]
assert release["components"]["npm"] == package["version"]
for host in (".codex-plugin", ".claude-plugin"):
    metadata = json.loads((plugin / host / "plugin.json").read_text())
    assert release["components"]["plugin"] == metadata["version"]
for name, expected in release["files"].items():
    path = Path(name)
    assert not path.is_absolute() and ".." not in path.parts and "\\" not in name
    target = root / path
    assert not any(p.is_symlink() for p in [target, *target.parents])
    assert hashlib.sha256(target.read_bytes()).hexdigest() == expected, (
        f"Release inventory mismatch: {name}"
    )

print(
    "Release versions/inventory, installer/plugin checksums, runtime modules, "
    "Skill identity and private-file exclusions passed."
)
