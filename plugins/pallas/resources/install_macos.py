"""Install a self-contained Pallas test bundle on a new Mac. Run with Python 3.12 or 3.13.

Core installation needs no media application identity. Live connections are optional.
No old workspaces, certificates or user OAuth tokens are imported.
"""

import argparse
import hashlib
import json
import subprocess
import sys
import venv
import zipfile
from pathlib import Path


def install(args):
    if sys.platform != "darwin" or sys.version_info[:2] not in ((3, 12), (3, 13)):
        raise ValueError(
            "Use Python 3.12 or 3.13 on macOS. The agent can install that prerequisite."
        )
    if args.meta_client_id and args.client != "codex":
        raise ValueError("Pre-registered Meta setup requires Codex.")
    if args.enable_meta and args.client == "codex" and not args.meta_client_id:
        raise ValueError("Codex live Meta requires an explicitly provided registered App ID.")
    if args.trust_local_certificate and not args.meta_client_id:
        raise ValueError("Certificate trust is only for explicit Codex Meta setup.")
    bundle = Path(__file__).resolve().parent
    wheels = list(bundle.glob("pallas_ads-*.whl"))
    if len(wheels) != 1:
        raise ValueError("The test bundle must contain exactly one Pallas wheel.")
    wheel = wheels[0]
    expected = json.loads((bundle / "release-manifest.json").read_text())
    if (
        expected["wheel"] != wheel.name
        or expected["sha256"] != hashlib.sha256(wheel.read_bytes()).hexdigest()
    ):
        raise ValueError("Wheel checksum mismatch; obtain a fresh bundle from the operator.")
    directory = args.directory.expanduser().absolute()
    if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
        raise ValueError("Choose a new or empty project directory; no existing state is replaced.")
    runtime = directory.with_name(directory.name + "-runtime")
    if runtime.exists():
        raise ValueError("The adjacent runtime already exists. Choose a new project name.")
    if args.require_google:
        with zipfile.ZipFile(wheel) as archive:
            name = "pallas_ads/resources/google-desktop.json"
            if name not in archive.namelist() or archive.getinfo(name).file_size > 65536:
                raise ValueError("Obtain a configured release wheel from the publisher.")
            app = json.loads(archive.read(name)).get("installed", {})
            if not app.get("client_id", "").endswith(".apps.googleusercontent.com") or not app.get(
                "client_secret"
            ):
                raise ValueError("Invalid release application configuration.")
    # Managed macOS Python distributions resolve libpython relative to their real
    # executable. Copying that executable into a venv can break its dylib path.
    venv.EnvBuilder(with_pip=True, symlinks=True).create(runtime)
    python = runtime / "bin/python"
    pallas = runtime / "bin/pallas"
    subprocess.run([str(python), "-m", "pip", "install", str(wheel)], check=True)
    command = [
        str(pallas),
        "agent",
        "setup",
        "--client",
        args.client,
        "--directory",
        str(directory),
    ]
    if args.enable_meta:
        command.extend(["--mode", "live"])
    if args.meta_client_id:
        command.extend(["--meta-client-id", args.meta_client_id])
    subprocess.run(command, check=True)
    if args.meta_client_id:
        command = [str(pallas), "agent", "prepare-meta", "--directory", str(directory)]
        if args.trust_local_certificate:
            command.append("--trust-local-certificate")
        subprocess.run(command, check=True)
    subprocess.run([str(pallas), "agent", "doctor", "--directory", str(directory)], check=True)
    print("Open this project in your Agent and start a new task:", directory)
    print("Local analysis is installed. Live media access is optional and separately verified.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--client", choices=["codex", "claude"], default="codex")
    parser.add_argument("--meta-client-id")
    parser.add_argument(
        "--enable-meta",
        action="store_true",
        help="Enable Claude host Meta; Codex requires --meta-client-id",
    )
    parser.add_argument("--require-google", action="store_true")
    parser.add_argument("--trust-local-certificate", action="store_true")
    args = parser.parse_args()
    try:
        install(args)
    except (ValueError, OSError, KeyError, subprocess.SubprocessError):
        # Third-party errors may contain sensitive input. Do not print traceback or JSON.
        print(
            "Installation incomplete. Check macOS/Python version, wheel checksum, embedded "
            "application configuration, fresh destination and system permissions. Existing files "
            "were not replaced. If a project was created, use its pallas agent doctor to resume "
            "the remaining setup; do not rerun over it.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
