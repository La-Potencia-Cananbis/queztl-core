#!/usr/bin/env python3
"""Minimal MCP-lite local tool server.

This module intentionally avoids heavy dependencies so it can run in constrained
or partially configured environments while still providing useful local tools.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.error
import urllib.request
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
    ok = all(bool(v) for k, v in checks.items() if k != "timestamp_utc")
    return ToolResult(ok=ok, tool="health_check", output=checks)


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


def run_content_once(repo_root: Path, execute: bool = False, theme: str = "revolutionary") -> ToolResult:
    """Run (or preview) one local content generation pass."""

    candidates = [
        repo_root / "backend" / "content_runner.py",
        repo_root / "nm-socialists-project" / "backend" / "content_runner.py",
    ]
    script = next((c for c in candidates if c.exists()), None)
    if script is None:
        return ToolResult(
            ok=False,
            tool="run_content_once",
            output={"error": "Missing content runner", "candidates": [str(c) for c in candidates]},
        )

    cmd = ["python3", str(script), "--single"]
    env = os.environ.copy()
    env["QUEZTL_CONTENT_THEME"] = theme

    if not execute:
        return ToolResult(
            ok=True,
            tool="run_content_once",
            output={
                "mode": "preview",
                "execute": False,
                "command": cmd,
                "env_overrides": {"QUEZTL_CONTENT_THEME": theme},
            },
        )

    proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True, env=env)
    return ToolResult(
        ok=proc.returncode == 0,
        tool="run_content_once",
        output={
            "mode": "executed",
            "returncode": proc.returncode,
            "stdout_tail": "\n".join(proc.stdout.splitlines()[-20:]),
            "stderr_tail": "\n".join(proc.stderr.splitlines()[-20:]),
        },
    )


def submit_contact_test(
    name: str = "Codex Test",
    email: str = "codex-test@example.com",
    phone: str = "000-000-0000",
    message: str = "MCP-lite contact test",
    member_type: str = "supporter",
    endpoint: str = "http://localhost:8003/submit",
) -> ToolResult:
    """Submit a local contact-form payload to the contact API."""

    payload = {
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "member_type": member_type,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=body, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode("utf-8", errors="replace")
            return ToolResult(
                ok=200 <= resp.status < 300,
                tool="submit_contact_test",
                output={"status": resp.status, "response": data, "endpoint": endpoint, "payload": payload},
            )
    except urllib.error.HTTPError as exc:
        return ToolResult(
            ok=False,
            tool="submit_contact_test",
            output={"error": "http_error", "status": exc.code, "body": exc.read().decode("utf-8", errors="replace")},
        )
    except Exception as exc:  # pragma: no cover - runtime/network dependent
        return ToolResult(ok=False, tool="submit_contact_test", output={"error": str(exc), "endpoint": endpoint})


def run_tool(tool_name: str, repo_root: Path, params: Dict[str, str], execute: bool) -> ToolResult:
    """Dispatch local tool execution."""

    if tool_name == "health_check":
        return health_check(repo_root)
    if tool_name == "list_memes":
        return list_memes(repo_root)
    if tool_name == "run_content_once":
        theme = params.get("theme", "revolutionary")
        return run_content_once(repo_root, execute=execute, theme=theme)
    if tool_name == "submit_contact_test":
        return submit_contact_test(
            name=params.get("name", "Codex Test"),
            email=params.get("email", "codex-test@example.com"),
            phone=params.get("phone", "000-000-0000"),
            message=params.get("message", "MCP-lite contact test"),
            member_type=params.get("member_type", "supporter"),
            endpoint=params.get("endpoint", "http://localhost:8003/submit"),
        )

    return ToolResult(
        ok=False,
        tool=tool_name,
        output={
            "error": f"Unknown tool '{tool_name}'",
            "available": ["health_check", "list_memes", "run_content_once", "submit_contact_test"],
        },
    )


def parse_params(raw_params: List[str]) -> Dict[str, str]:
    params: Dict[str, str] = {}
    for item in raw_params:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Queztl MCP-lite local server scaffold")
    parser.add_argument("--tool", default="health_check", help="Tool to execute locally")
    parser.add_argument("--repo-root", default=os.getcwd(), help="Repository root path")
    parser.add_argument("--json", action="store_true", help="Emit JSON output only")
    parser.add_argument("--execute", action="store_true", help="Allow execution for tools that support preview mode")
    parser.add_argument(
        "--param",
        action="append",
        default=[],
        help="Tool parameter in key=value format. Can be passed multiple times.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    params = parse_params(args.param)
    result = run_tool(args.tool, repo_root, params=params, execute=args.execute)

    payload = {"ok": result.ok, "tool": result.tool, "output": result.output}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"tool={result.tool} ok={result.ok}")
        print(json.dumps(result.output, indent=2, sort_keys=True))

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
