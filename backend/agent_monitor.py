#!/usr/bin/env python3
"""
Simple agent monitor for Queztl-Core
- Periodically (every 240s) runs quick checks via DistributedAgent
- Logs results to backend/agent_monitor.log
- Handles SIGINT/SIGTERM for graceful shutdown

Run: python3 -u backend/agent_monitor.py

"""
from __future__ import annotations

import json
import logging
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

# Ensure backend on path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from distributed_agent_wrapper import DistributedAgent, AgentPool
from queztl_config import config

# Configuration
INTERVAL_SECONDS = 240  # 4 minutes
LOG_PATH = ROOT / "agent_monitor.log"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("agent_monitor")

shutdown_requested = False


def handle_signal(signum, frame):
    global shutdown_requested
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    shutdown_requested = True


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def timestamp() -> str:
    from datetime import timezone
    return datetime.now(timezone.utc).isoformat()


def check_agent(agent: DistributedAgent) -> Dict:
    """Run simple capability and liveness checks on an agent and return a dict"""
    result: Dict = {"name": agent.name, "node": agent.node, "when": timestamp()}

    # Quick liveness check with timeout: run `echo ping`
    try:
        completed = agent.execute(["echo", "ping"], timeout=10)
        result["ping_returncode"] = completed.returncode
        result["ping_out"] = (completed.stdout or completed.stderr or "").strip()
        result["ok"] = completed.returncode == 0
    except Exception as exc:
        result["ping_error"] = str(exc)
        result["ok"] = False
        # Don't try capabilities if basic ping fails
        return result

    # Only check capabilities if ping succeeded
    if result["ok"]:
        try:
            # Use shorter Python check with timeout
            py_check = agent.run_python("import sys; print(sys.version.split()[0])", timeout=15)
            if py_check.returncode == 0:
                result["python_version"] = py_check.stdout.strip()
            else:
                result["python_error"] = py_check.stderr.strip()
        except Exception as exc:
            result["capabilities_error"] = str(exc)

    return result


def main() -> int:
    logger.info("Starting Queztl agent monitor")

    # Build a small pool of agents to monitor
    pool = AgentPool()

    # Create default agents — configurable later
    try:
        pool.create_agent("TrainerAgent", node="beast", use_docker=True)
        pool.create_agent("MonitorAgent", node="beast", use_docker=False)
    except Exception as e:
        logger.exception("Failed to create agents: %s", e)
        return 1

    logger.info("Agent pool: %s", pool)

    # Main loop
    iteration = 0
    while not shutdown_requested:
        iteration += 1
        logger.info("Monitor iteration %d: checking %d agents", iteration, len(pool.agents))

        for name, agent in pool.agents.items():
            try:
                res = check_agent(agent)
                logger.info(json.dumps(res, ensure_ascii=False))
            except Exception as e:
                logger.exception("Unhandled error checking agent %s: %s", name, e)

        # Sleep until next interval or until shutdown requested
        sleep_seconds = INTERVAL_SECONDS
        for _ in range(int(sleep_seconds)):
            if shutdown_requested:
                break
            time.sleep(1)

    logger.info("Monitor exiting cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
