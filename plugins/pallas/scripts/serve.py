"""Keep MCP discovery available while serializing workspace operations across hosts."""

import json
import os
import shutil
import sys
from pathlib import Path

from pallas_ads.mcp_server import serve
from pallas_ads.operations import Runtime, needs


class LockedRuntime(Runtime):
    def invoke(self, name, arguments):
        lock = self.workspace.layout.root / "plugin.lock"
        try:
            lock.mkdir(mode=0o700)
        except FileExistsError:
            return needs(
                name,
                "Pallas is busy in this project. Finish the other operation first; "
                "if a process crashed, inspect plugin.lock/owner.json before recovery.",
            )
        try:
            (lock / "owner.json").write_text(json.dumps({"pid": os.getpid()}))
            return super().invoke(name, arguments)
        finally:
            shutil.rmtree(lock)


if __name__ == "__main__":
    serve(LockedRuntime(Path(sys.argv[1])))
