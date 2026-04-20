#!/usr/bin/env python3
"""Minimal MCP-lite compatible local tool server scaffold.

This file intentionally provides a valid Python entrypoint so automation,
linters, and scanners can parse the project even when full MCP integration
is not yet wired.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ToolResult:
    """Simple structured result for local MCP-like tool calls."""

    ok: bool
    tool: str
    output: Dict[str, Any]


def health_check(repo_root: Path) -> ToolResult:
    """Return basic local repository and runtime health signals."""

    checks = {
        "repo_root_exists": repo_root.exists(),
        "backend_exists": (repo_root / "backend").exists(),
        "frontend_exists": (repo_root / "frontend").exists(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    return ToolResult(ok=all(bool(v) for k, v in checks.items() if k != "timestamp_utc"), tool="health_check", output=checks)


def list_memes(repo_root: Path) -> ToolResult:
    """List meme image files found in known project folders."""

    search_roots: List[Path] = [
        repo_root / "frontend-new" / "assets" / "img",
        repo_root / "nm-socialists-project" / "nm_socialists_modern" / "assets" / "img",
        repo_root / "nm-socialists-project" / "nm_socialists_original" / "assets" / "img",
    ]
    files: List[str] = []
    for folder in search_roots:
        if folder.exists():
            files.extend(str(p.relative_to(repo_root)) for p in sorted(folder.glob("meme_*.png")))

    return ToolResult(ok=True, tool="list_memes", output={"count": len(files), "files": files})


def run_tool(tool_name: str, repo_root: Path) -> ToolResult:
    """Dispatch local tool execution."""

    if tool_name == "health_check":
        return health_check(repo_root)
    if tool_name == "list_memes":
        return list_memes(repo_root)

    return ToolResult(
        ok=False,
        tool=tool_name,
        output={"error": f"Unknown tool '{tool_name}'", "available": ["health_check", "list_memes"]},
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Queztl MCP-lite local server scaffold")
    parser.add_argument("--tool", default="health_check", help="Tool to execute locally")
    parser.add_argument("--repo-root", default=os.getcwd(), help="Repository root path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output only")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    result = run_tool(args.tool, repo_root)

    payload = {"ok": result.ok, "tool": result.tool, "output": result.output}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"tool={result.tool} ok={result.ok}")
        print(json.dumps(result.output, indent=2, sort_keys=True))

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
