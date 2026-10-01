"""Publish only a reviewed tarball; usable locally or with npm trusted publishing."""

import argparse
import base64
import hashlib
import io
import json
import re
import subprocess
import tarfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REGISTRY = "https://registry.npmjs.org"


def version_key(version):
    match = re.fullmatch(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?",
        version,
    )
    if match is None:
        raise ValueError("Unsupported npm version; use a canonical semantic version.")
    prerelease = match[4]
    identifiers = []
    for part in prerelease.split(".") if prerelease else []:
        if part.isdigit() and len(part) > 1 and part.startswith("0"):
            raise ValueError("Numeric prerelease identifiers cannot have leading zeros.")
        identifiers.append((0, int(part)) if part.isdigit() else (1, part))
    return (int(match[1]), int(match[2]), int(match[3]), prerelease is None, tuple(identifiers))


def digest(data):
    return "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()


def read_url(url):
    if not url.startswith(REGISTRY + "/"):
        raise ValueError("Only the official npm registry is accepted.")
    with urllib.request.urlopen(url, timeout=30) as response:
        if not response.url.startswith(REGISTRY + "/"):
            raise ValueError("Unexpected registry redirect.")
        data = response.read(20 * 1024 * 1024 + 1)
    if len(data) > 20 * 1024 * 1024:
        raise ValueError("Registry response exceeds the release limit.")
    return data


def verify_archive(archive, manifest):
    archive = Path(archive)
    if archive.is_symlink():
        raise ValueError("Archive must be a regular file.")
    data = archive.read_bytes()
    if digest(data) != manifest["npm_tarball"]["integrity"]:
        raise ValueError("Tarball integrity differs from the reviewed manifest.")
    runtime = manifest["components"]["runtime"]
    wheel = f"resources/pallas_ads-{runtime}-py3-none-any.whl"
    allowed = {
        "package.json",
        "README.md",
        "LICENSE",
        "NOTICE",
        "bin/pallas-ads.mjs",
        "lib/installer.mjs",
        "resources/npm-runtime.json",
        "resources/release-manifest.json",
        "resources/install_macos.py",
        wheel,
    }
    if set(manifest["npm_files"]) != allowed:
        raise ValueError("Unexpected npm file inventory.")
    with tarfile.open(archive, "r:gz") as package:
        members = package.getmembers()
        if (
            len(members) != len(allowed)
            or {m.name for m in members} != {"package/" + n for n in allowed}
            or not all(m.isfile() and m.size <= 20 * 1024 * 1024 for m in members)
        ):
            raise ValueError("Tarball does not match the public file allowlist.")
        contents = {}
        for member in members:
            stream = package.extractfile(member)
            if stream is None:
                raise ValueError("Missing tarball file.")
            contents[member.name.removeprefix("package/")] = stream.read()
    metadata = json.loads(contents["package.json"])
    if metadata["name"] != "pallas-ads" or metadata["version"] != manifest["components"]["npm"]:
        raise ValueError("Package identity differs from the release manifest.")
    if any(k in metadata.get("scripts", {}) for k in ("preinstall", "install", "postinstall")):
        raise ValueError("Installation lifecycle hooks are not allowed.")
    if metadata.get("dependencies"):
        raise ValueError("Unexpected npm dependencies.")
    # README is specific to npm. All other bytes must match the public checkout inventory.
    for name, content in contents.items():
        expected = manifest["npm_files"][name]
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError(f"Package file checksum mismatch: {name}")
        if name != "README.md" and manifest["files"].get(name) != expected:
            raise ValueError(f"Package/public artifact mismatch: {name}")
    runtime_manifest = json.loads(contents["resources/npm-runtime.json"])
    if runtime_manifest["runtimeVersion"] != runtime:
        raise ValueError("Runtime version mismatch.")
    for name, expected in runtime_manifest["files"].items():
        if hashlib.sha256(contents["resources/" + name]).hexdigest() != expected:
            raise ValueError("Runtime resource mismatch.")
    with zipfile.ZipFile(io.BytesIO(contents[wheel])) as packaged_wheel:
        forbidden = {
            "PALLAS_HANDOFF.md",
            "PALLAS_PRODUCT.md",
            "PALLAS_PROJECT.md",
            "AGENTS.md",
            "google-desktop.json",
            ".env",
            ".pallas",
            "local_docs",
            "private_data",
            "__pycache__",
        }
        for name in packaged_wheel.namelist():
            parts = Path(name).parts
            if (
                name.startswith("/")
                or ".." in parts
                or forbidden.intersection(parts)
                or any(p.startswith(".env.") for p in parts)
                or name.endswith((".pem", ".key"))
            ):
                raise ValueError("Private or unsafe file in runtime wheel.")
    return data


def registry_status(manifest):
    version = manifest["components"]["npm"]
    try:
        metadata = json.loads(read_url(REGISTRY + "/pallas-ads"))
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return {"published": False, "latest": None}
        raise
    latest = metadata.get("dist-tags", {}).get("latest")
    package = metadata.get("versions", {}).get(version)
    if package is None:
        return {"published": False, "latest": latest}
    expected = manifest["npm_tarball"]["integrity"]
    if package["dist"]["integrity"] != expected:
        raise ValueError(
            "This npm version already exists with different bytes; choose a new version."
        )
    if digest(read_url(package["dist"]["tarball"])) != expected:
        raise ValueError("Downloaded registry tarball failed integrity verification.")
    return {
        "published": True,
        "latest": latest,
        "published_at": metadata.get("time", {}).get(version),
        "integrity": expected,
        "anonymous_download_verified": True,
    }


def publish(archive, manifest, *, promote=False):
    verify_archive(archive, manifest)
    before = registry_status(manifest)
    version = manifest["components"]["npm"]
    if (
        before.get("latest")
        and version_key(version) < version_key(before["latest"])
        and not promote
    ):
        raise ValueError("latest would move backwards; explicitly review and use --promote.")
    if before["published"]:
        if before["latest"] == version:
            return before
        if not promote:
            raise ValueError(
                "Matching version exists, but latest differs; explicitly use --promote."
            )
        command = ["npm", "dist-tag", "add", f"pallas-ads@{version}", "latest"]
    else:
        command = [
            "npm",
            "publish",
            str(Path(archive).absolute()),
            "--access",
            "public",
            "--tag",
            "latest",
            "--ignore-scripts",
        ]
    subprocess.run([*command, "--registry=" + REGISTRY], check=True)
    for attempt in range(12):
        result = registry_status(manifest)
        if result["published"] and result["latest"] == version:
            return result
        if attempt < 11:
            time.sleep(5)
    return {**result, "processing": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--promote", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    verify_archive(args.archive, manifest)
    result = (
        publish(args.archive, manifest, promote=args.promote)
        if args.publish
        else registry_status(manifest)
    )
    print(json.dumps(result, indent=2))
    if args.publish and result.get("processing"):
        raise SystemExit(75)


if __name__ == "__main__":
    main()
