"""Offline publication safety checks; never access npm or publisher credentials."""

import hashlib
import importlib.util
import io
import json
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "npm_publish.py"
if not SOURCE.exists():
    SOURCE = HERE.parent / "tools/npm_publish.py"
spec = importlib.util.spec_from_file_location("pallas_npm_publish_tested", SOURCE)
assert spec is not None and spec.loader is not None
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


def fixture(root, *, extra=None, private_wheel=False, applications=None, inventory=None):
    buffer = io.BytesIO()
    applications = applications or {}
    with zipfile.ZipFile(buffer, "w") as wheel:
        wheel.writestr("pallas_ads/__init__.py", '__version__ = "0.2.0a3"')
        if private_wheel:
            wheel.writestr("pallas_ads/resources/google-desktop.json", "synthetic private marker")
        for platform, content in applications.items():
            filename = {"google": "google-desktop.json", "meta": "meta-mcp.json"}[platform]
            wheel.writestr("pallas_ads/resources/" + filename, json.dumps(content))
    if inventory is None:
        inventory = {
            p: hashlib.sha256(json.dumps(content).encode()).hexdigest()
            for p, content in applications.items()
        }
    files = {
        "package.json": json.dumps({"name": "pallas-ads", "version": "0.2.0-alpha.4"}).encode(),
        "README.md": b"npm guide",
        "LICENSE": b"license",
        "NOTICE": b"notice",
        "bin/pallas-ads.mjs": b"// launcher",
        "lib/installer.mjs": b"// installer",
        "resources/pallas_ads-0.2.0a3-py3-none-any.whl": buffer.getvalue(),
        "resources/install_macos.py": b"# installer",
        "resources/release-manifest.json": json.dumps(
            {
                "google_application_embedded": "google" in applications,
                "oauth_applications": inventory,
            }
        ).encode(),
    }
    resources = {
        Path(k).name: hashlib.sha256(v).hexdigest()
        for k, v in files.items()
        if k.startswith("resources/")
    }
    files["resources/npm-runtime.json"] = json.dumps(
        {"runtimeVersion": "0.2.0a3", "files": resources}
    ).encode()
    archive = root / "package.tgz"
    with tarfile.open(archive, "w:gz") as tgz:
        for name, data in {**files, **(extra or {})}.items():
            member = tarfile.TarInfo("package/" + name)
            member.size = len(data)
            tgz.addfile(member, io.BytesIO(data))
    inventory = {k: hashlib.sha256(v).hexdigest() for k, v in files.items()}
    manifest = {
        "components": {"runtime": "0.2.0a3", "npm": "0.2.0-alpha.4", "plugin": "0.2.1"},
        "npm_tarball": {"integrity": publisher.digest(archive.read_bytes())},
        "npm_files": inventory,
        "files": {k: v for k, v in inventory.items() if k != "README.md"},
    }
    return archive, manifest


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.archive, self.manifest = fixture(self.root)

    def test_independent_versions_and_exact_inventory(self):
        self.assertEqual(
            publisher.verify_archive(self.archive, self.manifest), self.archive.read_bytes()
        )

    def test_changed_archive_is_rejected(self):
        self.archive.write_bytes(self.archive.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "integrity"):
            publisher.verify_archive(self.archive, self.manifest)

    def test_traversal_and_extra_files_are_rejected(self):
        for name in ("../escape", "AGENTS.md", ".npmrc"):
            with self.subTest(name=name):
                archive, manifest = fixture(self.root, extra={name: b"synthetic"})
                with self.assertRaisesRegex(ValueError, "allowlist"):
                    publisher.verify_archive(archive, manifest)

    def test_private_wheel_is_rejected(self):
        archive, manifest = fixture(self.root, private_wheel=True)
        with self.assertRaisesRegex(ValueError, "Private"):
            publisher.verify_archive(archive, manifest)

    def test_reviewed_publisher_applications_are_accepted(self):
        applications = {
            "google": {
                "installed": {
                    "client_id": "synthetic.apps.googleusercontent.com",
                    "client_secret": "synthetic-installed-client",
                }
            },
            "meta": {
                "client_id": "123456",
                "redirect_uri": "https://pallas-ads.com/oauth/meta/callback",
            },
        }
        archive, manifest = fixture(self.root, applications=applications)
        self.assertEqual(publisher.verify_archive(archive, manifest), archive.read_bytes())

    def test_application_tokens_and_other_redirects_are_rejected(self):
        for change in (
            {"access_token": "synthetic-never-publish"},
            {"redirect_uri": "https://example.com/callback"},
        ):
            with self.subTest(change=change):
                archive, manifest = fixture(
                    self.root,
                    applications={
                        "meta": {
                            "client_id": "123456",
                            "redirect_uri": "https://pallas-ads.com/oauth/meta/callback",
                            **change,
                        }
                    },
                )
                with self.assertRaisesRegex(ValueError, "Private"):
                    publisher.verify_archive(archive, manifest)

    def test_unlisted_application_is_rejected(self):
        archive, manifest = fixture(
            self.root,
            applications={
                "meta": {
                    "client_id": "123456",
                    "redirect_uri": "https://pallas-ads.com/oauth/meta/callback",
                }
            },
            inventory={},
        )
        with self.assertRaisesRegex(ValueError, "inventory"):
            publisher.verify_archive(archive, manifest)

    def test_changed_public_payload_is_rejected(self):
        self.manifest["files"]["lib/installer.mjs"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "public artifact"):
            publisher.verify_archive(self.archive, self.manifest)

    def test_same_version_different_registry_bytes_never_publishes(self):
        metadata = {"versions": {"0.2.0-alpha.4": {"dist": {"integrity": "different"}}}}
        with (
            patch.object(publisher, "read_url", return_value=json.dumps(metadata).encode()),
            patch.object(publisher.subprocess, "run") as command,
        ):
            with self.assertRaisesRegex(ValueError, "different bytes"):
                publisher.publish(self.archive, self.manifest)
            command.assert_not_called()

    def test_matching_publication_is_idempotent(self):
        status = {"published": True, "latest": "0.2.0-alpha.4"}
        with (
            patch.object(publisher, "registry_status", return_value=status),
            patch.object(publisher.subprocess, "run") as command,
        ):
            self.assertEqual(publisher.publish(self.archive, self.manifest), status)
            command.assert_not_called()

    def test_latest_is_not_silently_downgraded(self):
        status = {"published": True, "latest": "0.3.0"}
        with (
            patch.object(publisher, "registry_status", return_value=status),
            patch.object(publisher.subprocess, "run") as command,
        ):
            with self.assertRaisesRegex(ValueError, "--promote"):
                publisher.publish(self.archive, self.manifest)
            command.assert_not_called()

    def test_publish_uses_exact_tarball_and_checks_processing(self):
        complete = {"published": True, "latest": "0.2.0-alpha.4"}
        with (
            patch.object(
                publisher,
                "registry_status",
                side_effect=[{"published": False}, {"published": False}, complete],
            ),
            patch.object(publisher.subprocess, "run") as command,
            patch.object(publisher.time, "sleep"),
        ):
            self.assertEqual(publisher.publish(self.archive, self.manifest), complete)
            args = command.call_args.args[0]
            self.assertEqual(args[:3], ["npm", "publish", str(self.archive.absolute())])
            self.assertIn("--ignore-scripts", args)

    def test_non_registry_download_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "official"):
            publisher.read_url("https://example.com/package.tgz")

    def test_new_older_version_cannot_silently_downgrade_latest(self):
        with (
            patch.object(
                publisher, "registry_status", return_value={"published": False, "latest": "0.3.0"}
            ),
            patch.object(publisher.subprocess, "run") as command,
        ):
            with self.assertRaisesRegex(ValueError, "backwards"):
                publisher.publish(self.archive, self.manifest)
            command.assert_not_called()

    def test_semver_prerelease_order(self):
        ordered = ["0.2.0-alpha.2", "0.2.0-alpha.10", "0.2.0-beta.1", "0.2.0", "0.2.1"]
        self.assertEqual(sorted(reversed(ordered), key=publisher.version_key), ordered)

    def test_noncanonical_version_is_rejected(self):
        for value in ("latest", "0.2.0-alpha.01", "0.2.0-", "v0.2.0"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                publisher.version_key(value)


if __name__ == "__main__":
    unittest.main()
