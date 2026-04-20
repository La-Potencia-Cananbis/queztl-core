# Queztl Core Reincarnation Plan (April 20, 2026)

This is the execution blueprint for bringing Queztl back to a stable baseline that works:
1) on your current Mac via containers,
2) in cloud environments, and
3) later on your stronger hardware for scale.

The guiding rule is **portability first, scale second**.

---

## 1) Recovery targets (what success looks like)

By the end of this plan, we should have:

1. **Container-first local development** that does not depend on host-specific absolute paths.
2. **Cloud-deployable baseline stack** using the same container images and env contracts.
3. **Hardware-scale mode** that can switch execution providers to your local cluster when available.
4. **MCP that works in minimal mode** (single machine) with optional distributed backends.
5. **Graph-indexed project map** so decisions and dependencies are trackable.

---

## 2) What appears usable now

## Confirmed runnable building blocks

1. Website/service orchestration scripts exist:
   - `start-services.sh`
   - `stop-services.sh`
   - `setup-website.sh`

2. Core backend pieces for web flows exist:
   - `backend/contact_form_api.py`
   - `backend/content_runner.py`

3. NM Socialists assets are present in multiple variants:
   - `nm-socialists-project/`
   - `frontend-new/`

4. Infra and container scaffolding exists:
   - `infra/docker-compose.yml`
   - `infra/docker-compose.mac.yml`
   - `infra/git-container/docker-compose.yml`

---

## 3) Current blockers

## A) Documentation drift

Some docs reference machine-specific paths and old assumptions, creating startup confusion and false quickstarts.

## B) AIOSC/MCP implementation mismatch

- Architecture docs are detailed (`backend/AIOSC_ARCHITECTURE.md`).
- `backend/mcp_server.py` is currently not an executable implementation.
- `backend/aiosc_platform.py` is heavily commented out.
- `backend/deploy-aiosc.sh` contains host-specific hardcoded path assumptions.

## C) Product sprawl without canonical entrypoint

Multiple parallel tracks exist (Queztl core, NM Socialists, infra/git systems), but root-level canonical status and startup path are missing.

---

## 4) Execution roadmap (portable-first)

## Phase 0 (Day 1): Canonical status + graph baseline

1. Add `docs/CANONICAL_STATUS.md` with:
   - production_now
   - runnable_local
   - experimental
   - archived
2. Add graph index file `docs/REINCARNATION_GRAPH.yaml` (created in this PR).
3. Label major folders with lifecycle metadata (`ACTIVE`, `CANDIDATE`, `ARCHIVE`).

## Phase 1 (Days 2-3): Mac-to-container parity

Goal: nothing critical depends on host-only assumptions.

1. Remove hardcoded host paths from shell scripts (especially AIOSC deployment scripts).
2. Normalize scripts to repo-relative behavior (`$(cd "$(dirname "$0")" && pwd)` patterns).
3. Ensure all required services can be started via compose + one wrapper command.
4. Add a `doctor` check script to validate:
   - Docker daemon availability
   - required ports
   - required env vars
   - writable volumes

## Phase 2 (Days 3-5): MCP Lite (single-machine)

Implement a minimal functional MCP server with local tools:

1. `health_check()`
2. `run_content_once(theme)`
3. `list_memes()`
4. `submit_contact_test(payload)`

This restores MCP utility without requiring Beast/Sloth.

## Phase 3 (Week 2): Cloud baseline

1. Build images once, deploy same images to cloud target.
2. Move all config to env/secret management (no machine-bound values).
3. Stand up baseline services in cloud:
   - API
   - static frontend
   - optional worker service
4. Add simple provider flaging:
   - `EXECUTION_PROVIDER=local|cloud|cluster`

## Phase 4 (Week 3+): Hardware scale mode

When stronger hardware is ready:

1. Add cluster adapters behind provider interface.
2. Keep MCP tool surface stable; only backend provider changes.
3. Route heavy jobs to local hardware, keeping cloud as fallback.

---

## 5) Mac containerization task list (explicit)

These are now tracked as first-class tasks:

- [ ] Task M1: Containerize all host-coupled scripts used by quickstarts.
- [ ] Task M2: Replace absolute host paths in deploy scripts with repo-relative logic.
- [ ] Task M3: Define persistent volumes for generated content, DB, logs.
- [ ] Task M4: Pin Python + Node runtime versions in containers.
- [ ] Task M5: Verify `docker compose up` brings a useful default stack on Mac.
- [ ] Task M6: Add smoke script that runs inside container network.

---

## 6) Cloud-first then hardware-scale strategy

## Deployment model

1. **Base mode (cloud)**: reliable, always-on, moderate performance.
2. **Scale mode (your strong hardware)**: high-performance jobs moved off cloud.
3. **Fallback policy**: if hardware provider unavailable, route to cloud provider.

## Provider contract (recommended)

Each provider should implement:

- `run_job(job_type, payload)`
- `get_health()`
- `get_capacity()`
- `cancel_job(job_id)`

Then select provider by configuration, not by rewriting workflows.

---

## 7) Graph-structured reference model

To support your list/graph way of working, this plan now uses a graph index:

- Node types:
  - `service`
  - `script`
  - `doc`
  - `deployment_target`
  - `risk`
  - `task`
- Edge types:
  - `depends_on`
  - `implements`
  - `blocked_by`
  - `deploys_to`
  - `verifies`

The graph seed lives in `docs/REINCARNATION_GRAPH.yaml` and is intended to be extended as cleanup progresses, including one child graph per major node.

---


## 7.1) Per-node subgraphs + agent completion loop

Yes — this is exactly the right model.

Each major node in the main graph should own a child graph that tests and validates one function/output at a time.

- Parent graph: `docs/REINCARNATION_GRAPH.yaml`
- Node workflow: `docs/NODE_GRAPH_WORKFLOW.md`
- Child graph location: `docs/node-graphs/<node_id>.yaml`

Completion rule: a parent node is complete only when its child graph reaches done with passing test evidence.

## 8) Immediate next actions (ordered)

1. Convert AIOSC deploy logic to repo-relative and container-safe.
2. Stand up local compose baseline and run smoke checks.
3. Implement minimal working MCP server (local provider).
4. Generate and validate dead-link report for markdown.
5. Promote one root quickstart and archive stale alternatives.

---

## 9) Definition of done (reincarnation milestone)

You can call this reincarnated when:

1. New contributor can run one root quickstart and succeed on Mac with Docker.
2. Same containers can be deployed to cloud with env-only differences.
3. MCP works locally and supports provider switching.
4. Heavy workloads can later be redirected to your strong hardware with no MCP contract changes.
5. Graph index is updated as the single dependency/reference map.
