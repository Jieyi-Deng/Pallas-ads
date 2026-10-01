"""Offline black-box command acceptance against an installed wheel and a built plugin.

Uses synthetic confirmation only, separate project bindings and a new MCP process per call.
Does not load a host model, authorize media, or access customer data.
"""

import argparse
import csv
import json
import subprocess
from decimal import Decimal
from pathlib import Path


def check(python: Path, plugin: Path, output: Path):
    python, plugin, output = python.absolute(), plugin.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    installed = subprocess.run(
        [str(python), "-I", "-c", "import pallas_ads.command; print(pallas_ads.command.__file__)"],
        cwd=output,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert "site-packages" in Path(installed).parts, installed
    manifest = json.loads((plugin / "resources/npm-runtime.json").read_text())
    wheel_hash = manifest["files"][manifest["wheel"]]
    version = json.loads((plugin / ".codex-plugin/plugin.json").read_text())["version"]
    summaries = {}
    for client in ("codex", "claude"):
        project = output / client
        project.mkdir()
        subprocess.run(
            [
                str(python),
                str(plugin / "scripts/project.py"),
                "setup",
                str(project),
                client,
                str(python.parent.parent),
                version,
                wheel_hash,
                "node",
                "--install-command",
            ],
            cwd=output,
            capture_output=True,
            text=True,
            check=True,
        )
        skill_root = ".agents/skills" if client == "codex" else ".claude/skills"
        alias = (project / skill_root / "pallas/SKILL.md").read_text()
        assert str(plugin / "skills/pallas/SKILL.md") in alias

        def invoke(payload, *, project=project):
            frames = [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-11-25",
                        "capabilities": {},
                        "clientInfo": {"name": "synthetic-command-check"},
                    },
                },
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": "pallas_command", "arguments": payload},
                },
            ]
            process = subprocess.run(
                [str(python), str(plugin / "scripts/serve.py"), str(project / ".pallas")],
                cwd=project,
                input="\n".join(map(json.dumps, frames)) + "\n",
                text=True,
                capture_output=True,
                check=True,
                timeout=60,
            )
            assert not process.stderr, process.stderr
            replies = [json.loads(line) for line in process.stdout.splitlines()]
            assert len(replies[1]["result"]["tools"]) == 11
            return replies[-1]["result"]["structuredContent"]

        def import_export(platform, dates, *, project=project, invoke=invoke):
            path = project / f"synthetic-{platform}.csv"
            with path.open("w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(
                    [
                        "date",
                        "account_id",
                        "campaign_id",
                        "campaign_name",
                        "spend",
                        "impressions",
                        "clicks",
                        "currency",
                        "timezone",
                    ]
                )
                for day in dates:
                    writer.writerow(
                        [day, "123", "001", "SYNTHETIC", "10.25", 1000, 10, "USD", "UTC"]
                    )
            file = {"file_path": str(path), "import_options": {"platform": platform}}
            preview = invoke({"intent": "analysis", "file": file})
            assert preview["status"] == "pending_user_action", preview
            result = invoke(
                {
                    "intent": "analysis",
                    "file": {
                        **file,
                        "review_hash": preview["result"]["details"]["review_hash"],
                        "user_confirmed": True,
                    },
                }
            )
            assert result["status"] == "partial_result", result
            assert result["result"]["validation"]["verified"]
            assert Path(result["result"]["artifacts"]["html"]).is_file()
            assert Decimal(result["result"]["details"]["diagnostics"]["totals"]["spend"]) == (
                Decimal("10.25") * len(dates)
            )
            return result["result"]["details"]["dataset_id"]

        assert invoke({"intent": "status"})["result"]["workspace_state"] == "ready"
        datasets = {
            p: import_export(p, ["2026-09-28", "2026-09-29"]) for p in ("google", "meta", "tiktok")
        }
        ingests = [{"source_key": p + ":123", "dataset_id": value} for p, value in datasets.items()]
        created = invoke(
            {
                "intent": "dashboard",
                "dashboard": {
                    "op": "create",
                    "dashboard_id": "dash_install",
                    "title": "SYNTHETIC install check",
                    "as_of": "2026-09-30",
                    "ingest": ingests,
                    "sources": [
                        {"platform": p, "account_id": "123", "route": "file_import"}
                        for p in datasets
                    ],
                },
            }
        )
        assert created["status"] == "complete", created
        assert created["result"]["validation"]["verified"]
        assert created["result"]["details"]["row_count"] == 6
        repeated = invoke(
            {"intent": "dashboard", "dashboard": {"as_of": "2026-09-30", "ingest": ingests}}
        )
        assert repeated["result"]["details"]["row_count"] == 6
        assert all(
            o["inserted"] == o["restated"] == o["removed"] == 0
            for o in repeated["result"]["details"]["run"]["sources"].values()
        )
        updated_dataset = import_export("google", ["2026-09-30"])
        updated = invoke(
            {
                "intent": "update",
                "dashboard": {
                    "dashboard_id": "dash_install",
                    "as_of": "2026-10-01",
                    "ingest": [{"source_key": "google:123", "dataset_id": updated_dataset}],
                },
            }
        )
        assert updated["status"] == "partial_result", updated  # other files are now stale
        assert updated["result"]["validation"]["verified"]
        assert updated["result"]["details"]["row_count"] == 7
        assert len(list((project / ".pallas/dashboards").glob("dash_*/state.json"))) == 1
        summaries[client] = {
            "analysis_platforms": list(datasets),
            "initial_rows": 6,
            "repeated_rows": 6,
            "new_process_updated_rows": 7,
            "stale_other_sources": "partial_result",
            "artifact_integrity": True,
            "project_alias": True,
            "host_model_tested": False,
        }
    summary = {
        "evidence": "installed wheel + plugin scripts/MCP, synthetic only",
        "clients": summaries,
    }
    (output / "RESULTS.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    check(args.python, args.plugin, args.output)
