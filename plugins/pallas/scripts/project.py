"""Project binding and reversible migration; never reads host credential stores."""

import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import tomllib
from datetime import UTC, datetime
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(project, relative):
    path = project / relative
    if not path.is_relative_to(project) or ".." in path.parts:
        raise ValueError("Invalid project path")
    for item in [path, *path.parents]:
        if item == project:
            break
        if item.is_symlink():
            raise ValueError("Configuration or state paths must not be symlinks")
    return path


def tree_digest(path):
    files = []
    for item in sorted(path.rglob("*")):
        if item.is_symlink():
            raise ValueError("Skill symlinks require manual migration")
        if item.is_file():
            files.append((str(item.relative_to(path)), digest(item.read_bytes())))
    return digest(json.dumps(files).encode())


def encode(value):
    return (json.dumps(value, indent=2) + "\n").encode()


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(dir=path.parent, prefix=".pallas-write-")
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def transaction(project, updates, moves=()):
    """Preflight all inputs, journal originals, then apply with error rollback."""
    updates = {
        k: v
        for k, v in updates.items()
        if not safe(project, k).exists() or safe(project, k).read_bytes() != v
    }
    if not updates and not moves:
        return None
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    backup = safe(project, ".pallas/plugin-backups/" + stamp)
    records, directories = [], []
    for relative, data in updates.items():
        path = safe(project, relative)
        before = path.read_bytes() if path.exists() else None
        records.append(
            {
                "path": relative,
                "before": None if before is None else before.hex(),
                "after": digest(data),
            }
        )
    for relative in moves:
        path = safe(project, relative)
        directories.append({"path": relative, "hash": tree_digest(path)})
    backup.mkdir(parents=True, exist_ok=False)
    atomic(backup / "changes.json", encode({"files": records, "directories": directories}))
    done, moved = [], []
    try:
        for row in records:
            atomic(safe(project, row["path"]), updates[row["path"]])
            done.append(row)
        for row in directories:
            destination = backup / "directories" / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            safe(project, row["path"]).rename(destination)
            moved.append(row)
    except BaseException:
        for row in reversed(moved):
            (backup / "directories" / row["path"]).rename(safe(project, row["path"]))
        for row in reversed(done):
            target = safe(project, row["path"])
            if row["before"] is None:
                target.unlink(missing_ok=True)
            else:
                atomic(target, bytes.fromhex(row["before"]))
        raise
    atomic(safe(project, ".pallas/plugin-last-change.json"), encode({"backup": stamp}))
    return stamp


def remove_codex_server(text):
    # Keep every other TOML section byte-for-byte. Parse before and after editing.
    original = tomllib.loads(text)
    result, skipping = [], False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("["):
            section = line.strip().split("#")[0].strip()
            skipping = bool(
                re.fullmatch(r'\[mcp_servers\.(?:pallas|"pallas")(?:\.[^\]]+)?\]', section)
            )
        if not skipping:
            result.append(line)
    changed = "".join(result)
    actual = tomllib.loads(changed)
    expected = json.loads(json.dumps(original))
    expected.get("mcp_servers", {}).pop("pallas", None)
    # Empty parent table may disappear if it was only implicit.
    if not expected.get("mcp_servers"):
        expected.pop("mcp_servers", None)
    if not actual.get("mcp_servers"):
        actual.pop("mcp_servers", None)
    if actual != expected:
        raise ValueError("Nonstandard TOML needs manual migration; nothing changed")
    return changed


def setup(project, client, runtime, version, wheel_hash, migrate, node="node"):
    from pallas_ads.local_state import WorkspaceRepository

    updates, moves = {}, []
    config_name = ".mcp.json" if client == "claude" else ".codex/config.toml"
    config_path = safe(project, config_name)
    config = {}
    if config_path.exists():
        config = (
            json.loads(config_path.read_text())
            if client == "claude"
            else tomllib.loads(config_path.read_text())
        )
    server = config.get("mcpServers" if client == "claude" else "mcp_servers", {}).get("pallas")
    skill_root = ".claude/skills" if client == "claude" else ".agents/skills"
    for name in ["pallas-workflow", "pallas-analysis"]:
        relative = skill_root + "/" + name
        path = safe(project, relative)
        if path.exists():
            moves.append(relative)
    binding_path = safe(project, ".pallas/plugin-install.json")
    binding = json.loads(binding_path.read_text()) if binding_path.exists() else {}
    if binding and (binding.get("client") != client or binding.get("project") != str(project)):
        raise ValueError("This binding belongs to another client/path; keep separate projects.")
    managed_server = client == "codex" and server and server == binding.get("mcp")
    if binding.get("mcp") and server and not managed_server:
        raise ValueError("Pallas MCP config was customized after setup. Review it manually.")
    if ((server and not managed_server) or moves) and not migrate:
        raise ValueError(
            "Existing project Pallas configuration/Skills found. "
            "Run setup with --migrate to back them up and switch to the plugin."
        )
    if server and not managed_server:
        receipt_path = safe(project, ".pallas/npm-install.json")
        if not receipt_path.exists():
            raise ValueError("Custom Pallas MCP config: migrate it manually after review.")
        receipt = json.loads(receipt_path.read_text())
        expected_runtime = str(project) + "-runtime"
        if (
            receipt.get("project") != str(project)
            or receipt.get("client") != client
            or receipt.get("runtime") != expected_runtime
            or server.get("command") != expected_runtime + "/bin/pallas"
            or server.get("args") != ["mcp", "serve", "--workspace", str(project / ".pallas")]
            or set(server) - {"command", "args", "type", "tool_timeout_sec"}
            or server.get("type", "stdio") != "stdio"
            or server.get("tool_timeout_sec", 180) != 180
        ):
            raise ValueError(
                "Existing MCP differs from the npm-generated configuration. Nothing changed."
            )
        if client == "claude":
            del config["mcpServers"]["pallas"]
            updates[config_name] = encode(config)
        else:
            updates[config_name] = remove_codex_server(config_path.read_text()).encode()
    mcp = None
    if client == "codex":
        # Codex legacy plugin MCP does not expand Claude's package-root variable.
        # Bind one project server explicitly; Skills still load through the native plugin.
        launcher = str(Path(__file__).resolve().with_name("pallas.mjs"))
        mcp = {
            "command": node,
            "args": [launcher, "serve", "--project", str(project)],
            "env_vars": ["PALLAS_DATA_HOME"],
            "startup_timeout_sec": 15,
            "tool_timeout_sec": 180,
        }
        raw = config_path.read_text() if config_path.exists() else ""
        if server:
            raw = remove_codex_server(raw)
        section = (
            "\n[mcp_servers.pallas]\n"
            + "\n".join(key + " = " + json.dumps(value) for key, value in mcp.items())
            + "\n"
        )
        updates[config_name] = (raw.rstrip() + section).lstrip("\n").encode()
    instruction_name = "CLAUDE.md" if client == "claude" else "AGENTS.md"
    instructions = safe(project, instruction_name)
    if not instructions.exists():
        updates[instruction_name] = (
            b"# Pallas project\n\nUse the installed Pallas plugin and its pallas-workflow and "
            b"pallas-analysis Skills. Keep data in this project's .pallas workspace. "
            b"Authorize media through the configured host connection. Never copy tokens or "
            b"modify campaigns. File analysis can skip authorization.\n"
        )
    else:
        old = instructions.read_text()
        new = re.sub(
            r"For Pallas work, read `[^`]+/pallas-workflow/SKILL.md`\.",
            "For Pallas work, use the installed plugin's pallas-workflow Skill.",
            old,
        )
        if new != old:
            updates[instruction_name] = new.encode()
    gitignore = safe(project, ".gitignore")
    content = gitignore.read_text() if gitignore.exists() else ""
    if ".pallas/" not in content.splitlines():
        updates[".gitignore"] = (content.rstrip() + "\n.pallas/\n").lstrip("\n").encode()
    updates[".pallas/plugin-install.json"] = encode(
        {
            "project": str(project),
            "client": client,
            "pluginVersion": version,
            "wheelSha256": wheel_hash,
            "schemaVersion": 1,
            "mcp": mcp,
        }
    )
    # No secrets are copied. Existing .pallas data is opened in place, not reset.
    repository = WorkspaceRepository(project / ".pallas")
    if repository.layout.workspace_file.exists():
        repository.load_manifest()
    else:
        repository.bootstrap("workspace_" + digest(str(project).encode())[:16])
    backup = transaction(project, updates, moves)
    print(
        json.dumps(
            {
                "status": "ready",
                "project": str(project),
                "backup": backup,
                "runtime": runtime,
                "next": "Reload plugins in this project.",
            }
        )
    )


def rollback(project):
    pointer = safe(project, ".pallas/plugin-last-change.json")
    stamp = json.loads(pointer.read_text())["backup"]
    if not re.fullmatch(r"\d{8}T\d{12}Z", stamp):
        raise ValueError("Invalid backup identifier")
    backup = safe(project, ".pallas/plugin-backups/" + stamp)
    records = json.loads((backup / "changes.json").read_text())
    for row in records["files"]:
        path = safe(project, row["path"])
        if not path.is_file() or digest(path.read_bytes()) != row["after"]:
            raise ValueError(
                "Files changed after setup. Review the backup; rollback will not overwrite them."
            )
    for row in records["directories"]:
        target = safe(project, row["path"])
        archived = safe(project, str((backup / "directories" / row["path"]).relative_to(project)))
        if target.exists() or not archived.is_dir() or tree_digest(archived) != row["hash"]:
            raise ValueError("Skill paths changed after setup. Review the backup manually.")
    for row in records["files"]:
        target = safe(project, row["path"])
        if row["before"] is None:
            target.unlink()
        else:
            atomic(target, bytes.fromhex(row["before"]))
    for row in records["directories"]:
        target = safe(project, row["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        (backup / "directories" / row["path"]).rename(target)
    pointer.unlink()
    print(
        "Previous project configuration restored. "
        "Disable the native plugin before reloading a restored npm installation. "
        "Analysis data was retained."
    )


def deactivate(project):
    binding = json.loads(safe(project, ".pallas/plugin-install.json").read_text())
    if binding["client"] == "codex":
        path = safe(project, ".codex/config.toml")
        raw = path.read_text() if path.exists() else ""
        server = tomllib.loads(raw).get("mcp_servers", {}).get("pallas")
        if server:
            if server != binding.get("mcp"):
                raise ValueError("Pallas MCP config was customized; review before deactivation.")
            transaction(project, {".codex/config.toml": remove_codex_server(raw).encode()})
    print(
        "Project entry deactivated. Disable/uninstall Pallas in the host, then reload. "
        "Local analysis data and media authorizations were retained."
    )


def connect_meta(project):
    binding = json.loads(safe(project, ".pallas/plugin-install.json").read_text())
    if binding["client"] != "claude":
        raise ValueError(
            "Codex Meta needs the supported preregistered setup. "
            "Contact support@pallas-ads.com; existing host authorization is not changed."
        )
    config_path, settings_path = safe(project, ".mcp.json"), safe(project, ".claude/settings.json")
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}
    servers = config.setdefault("mcpServers", {})
    expected = {"type": "http", "url": "https://mcp.facebook.com/ads"}
    if "meta_official" in servers and servers["meta_official"] != expected:
        raise ValueError("Existing Meta configuration differs; retain it and review manually.")
    servers["meta_official"] = expected

    command = (
        shlex.quote(str(Path(sys.executable).absolute().with_name("pallas"))) + " agent guard-meta"
    )
    hook = {"matcher": "mcp__meta_official__.*", "hooks": [{"type": "command", "command": command}]}
    hooks = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])
    # Preserve other hooks. Only add our read guard if it is not already present.
    if hook not in hooks:
        hooks.append(hook)
    backup = transaction(
        project, {".mcp.json": encode(config), ".claude/settings.json": encode(settings)}
    )
    print(
        json.dumps(
            {
                "status": "configuration_ready",
                "backup": backup,
                "next": "Reload and trust project MCP and hooks; "
                "/mcp -> meta_official -> Authenticate. Review consent, then discover accounts. "
                "No authorization was performed.",
            }
        )
    )


if __name__ == "__main__":
    try:
        command, raw_project, *args = sys.argv[1:]
        project = Path(raw_project).resolve()
        if command == "setup":
            client, runtime, version, wheel_hash, node, *flags = args
            setup(project, client, runtime, version, wheel_hash, flags == ["--migrate"], node)
        elif command == "rollback":
            rollback(project)
        elif command == "deactivate":
            deactivate(project)
        elif command == "connect-meta":
            connect_meta(project)
        else:
            raise ValueError("Unknown project operation")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("Pallas project setup: " + str(exc), file=sys.stderr)
        raise SystemExit(1) from None
