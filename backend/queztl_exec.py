"""Command execution helpers with command-center guardrails.

Queztl has a hard rule: the command-center (typically the macOS laptop)
must not run heavy compute locally. This module centralizes that policy
and provides a small abstraction for running commands:

- local: run via subprocess on the current machine
- ssh: run via ssh on a remote host
- docker: run via docker exec on the current machine
- ssh_docker: run docker exec on a remote host over ssh

Configuration is via environment variables (or explicit args):
- QUEZTL_EXEC_MODE: local|ssh|docker|ssh_docker
- QUEZTL_SSH_USER: ssh username (default: xava)
- QUEZTL_SSH_HOST: ssh host (IP/hostname)
- QUEZTL_DOCKER_CONTAINER: docker container name/id (e.g. ray-head)
- QUEZTL_REMOTE_CWD: working dir on remote when using ssh/ssh_docker
- QUEZTL_ALLOW_LOCAL_COMPUTE: set to '1' to allow local execution even on mac

This is intentionally minimal and dependency-free.
"""

from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

try:
    # Package import (recommended): python -m backend.<module>
    from backend.queztl_discovery import is_command_center, ssh_user
except ImportError:  # pragma: no cover
    # Script import fallback: python backend/<module>.py
    from queztl_discovery import is_command_center, ssh_user



class ExecMode(str, Enum):
    LOCAL = "local"
    SSH = "ssh"
    DOCKER = "docker"
    SSH_DOCKER = "ssh_docker"


@dataclass
class ExecConfig:
    mode: ExecMode
    ssh_host: Optional[str] = None
    ssh_user: str = "xava"
    docker_container: Optional[str] = None
    remote_cwd: Optional[str] = None


class ExecError(RuntimeError):
    pass


def _quote_cmd(cmd: List[str]) -> str:
    return " ".join(shlex.quote(c) for c in cmd)


def default_exec_config() -> ExecConfig:
    mode = ExecMode(os.environ.get("QUEZTL_EXEC_MODE", ExecMode.LOCAL.value))
    return ExecConfig(
        mode=mode,
        ssh_host=os.environ.get("QUEZTL_SSH_HOST"),
        ssh_user=ssh_user(),
        docker_container=os.environ.get("QUEZTL_DOCKER_CONTAINER"),
        remote_cwd=os.environ.get("QUEZTL_REMOTE_CWD"),
    )


class CommandExecutor:
    def __init__(self, config: Optional[ExecConfig] = None):
        self.config = config or default_exec_config()

    def _enforce_policy(self):
        if self.config.mode == ExecMode.LOCAL and is_command_center() and os.environ.get("QUEZTL_ALLOW_LOCAL_COMPUTE") != "1":
            raise ExecError(
                "Local execution is disabled on command-center. "
                "Set QUEZTL_EXEC_MODE to ssh/docker/ssh_docker, "
                "or (not recommended) set QUEZTL_ALLOW_LOCAL_COMPUTE=1."
            )

    def run(
        self,
        cmd: List[str],
        *,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        capture_output: bool = True,
        text: bool = True,
        timeout: Optional[int] = None,
        check: bool = False,
    ) -> subprocess.CompletedProcess:
        self._enforce_policy()

        mode = self.config.mode

        if mode == ExecMode.LOCAL:
            return subprocess.run(
                cmd,
                cwd=cwd,
                env=env,
                capture_output=capture_output,
                text=text,
                timeout=timeout,
                check=check,
            )

        if mode == ExecMode.DOCKER:
            if not self.config.docker_container:
                raise ExecError("QUEZTL_DOCKER_CONTAINER is required for docker mode")
            docker_cmd = ["docker", "exec"]
            if cwd:
                docker_cmd += ["-w", cwd]
            docker_cmd += [self.config.docker_container] + cmd
            return subprocess.run(
                docker_cmd,
                env=env,
                capture_output=capture_output,
                text=text,
                timeout=timeout,
                check=check,
            )

        if mode in (ExecMode.SSH, ExecMode.SSH_DOCKER):
            if not self.config.ssh_host:
                raise ExecError("QUEZTL_SSH_HOST is required for ssh/ssh_docker mode")
            user = self.config.ssh_user
            host = self.config.ssh_host

            remote_cwd = self.config.remote_cwd
            effective_cwd = remote_cwd or cwd

            remote_inner_cmd: List[str]
            if mode == ExecMode.SSH:
                remote_inner_cmd = cmd
            else:
                if not self.config.docker_container:
                    raise ExecError("QUEZTL_DOCKER_CONTAINER is required for ssh_docker mode")
                remote_inner_cmd = ["docker", "exec"]
                if effective_cwd:
                    remote_inner_cmd += ["-w", effective_cwd]
                remote_inner_cmd += [self.config.docker_container] + cmd
                # In ssh_docker mode we don't additionally apply cwd at ssh level.
                effective_cwd = None

            # For ssh_docker mode, we need to properly quote the entire docker command
            # as a single argument to SSH, otherwise the remote shell doesn't parse it correctly
            if mode == ExecMode.SSH_DOCKER:
                # Build the docker command as a properly quoted shell string
                docker_shell_cmd = _quote_cmd(remote_inner_cmd)
                ssh_cmd = [
                    "ssh",
                    "-o",
                    "BatchMode=yes",
                    "-o",
                    "ConnectTimeout=10",
                    f"{user}@{host}",
                    docker_shell_cmd  # Single string argument with full docker command
                ]
            else:
                # For regular SSH mode, use bash -lc to get login environment
                remote_shell = _quote_cmd(remote_inner_cmd)
                if effective_cwd:
                    remote_shell = f"cd {shlex.quote(effective_cwd)} && {remote_shell}"

                ssh_cmd = [
                    "ssh",
                    "-o",
                    "BatchMode=yes",
                    "-o",
                    "ConnectTimeout=10",
                    f"{user}@{host}",
                    "bash",
                    "-lc",
                    remote_shell,
                ]

            return subprocess.run(
                ssh_cmd,
                env=env,
                capture_output=capture_output,
                text=text,
                timeout=timeout,
                check=check,
            )

        raise ExecError(f"Unknown exec mode: {mode}")
