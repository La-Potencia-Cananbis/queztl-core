from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from .agent import EchoAgent
from .models import GraphNode, GraphSpec
from .scheduler import KernelScheduler
from .store import KernelStore


def build_demo_graph() -> GraphSpec:
    return GraphSpec(
        name="demo-echo-dag",
        nodes=[
            GraphNode(
                id="source",
                packet_type="echo.say",
                payload={"text": "P0 source injection"},
            ),
            GraphNode(
                id="transform",
                packet_type="echo.say",
                payload={"text": "P1 topology transform"},
                depends_on=["source"],
            ),
            GraphNode(
                id="lock",
                packet_type="echo.say",
                payload={"text": "P4 signal lock"},
                depends_on=["transform"],
            ),
        ],
    )


async def run_demo(db_path: str) -> None:
    store = KernelStore(db_path)
    scheduler = KernelScheduler(store)
    scheduler.register_agent(EchoAgent(store))
    await scheduler.start_agents()
    try:
        result = await scheduler.run_graph(build_demo_graph())
        print(json.dumps(result, indent=2))
    finally:
        await scheduler.stop_agents()


def main() -> None:
    parser = argparse.ArgumentParser(description="Quetzl Agent Kernel V3")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="run built-in demo graph")
    demo.add_argument("--db", default="quetzl_kernel.db")

    args = parser.parse_args()
    if args.command == "demo":
        asyncio.run(run_demo(args.db))


if __name__ == "__main__":
    main()
