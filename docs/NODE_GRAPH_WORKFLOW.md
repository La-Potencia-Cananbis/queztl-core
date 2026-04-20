# Node Graph Workflow (Function-by-Function Validation)

This workflow lets each **major node** in the reincarnation graph have its own subgraph and test loop.

## Core idea

- Parent graph tracks major outcomes.
- Each major node points to a child graph file.
- An agent iterates the child graph until acceptance criteria pass.
- Parent node is marked complete only when child graph reports success.

---

## 1) Parent -> Child graph relationship

In `docs/REINCARNATION_GRAPH.yaml`, a major task node should include:

- `child_graph`: path to node-level graph file
- `acceptance_ref`: checklist or test criteria id
- `rollup_rule`: how completion is determined

Example:

```yaml
- id: task_mcp_lite
  type: task
  status: in_progress
  child_graph: docs/node-graphs/task_mcp_lite.yaml
  acceptance_ref: acc_mcp_lite_v1
  rollup_rule: all_child_tasks_complete_and_tests_green
```

---

## 2) Child graph structure

Each child graph should include:

- `scope`: what function/output this node must satisfy
- `inputs`: dependencies and fixtures
- `tasks`: incremental implementation tasks
- `tests`: explicit checks and expected outcomes
- `exit_criteria`: must-pass list
- `status`: `todo|in_progress|blocked|done`

Recommended file location:
- `docs/node-graphs/<parent_node_id>.yaml`

---

## 3) Agent iteration loop

Use this loop for each child graph:

1. Read child graph.
2. Pick first `todo` or `blocked` task with solvable dependency.
3. Implement change.
4. Run mapped tests.
5. Update node/task status.
6. Repeat until `exit_criteria` all pass.
7. Update parent node status to `done` in main graph.

---

## 4) Completion policy

A parent graph node may be marked complete only if all are true:

1. Child graph `status: done`.
2. All child `tests` marked pass.
3. No unresolved `blocked` child tasks.
4. Evidence is attached (command outputs, file refs, or report links).

---

## 5) Suggested status semantics

- `todo`: not started
- `in_progress`: active work
- `blocked`: cannot proceed pending dependency
- `done`: validated complete
- `verified`: done + independently validated

---

## 6) Minimal child graph template

```yaml
version: 1
node_id: task_example
scope: "Implement example capability"
status: todo

inputs:
  - file: backend/example.py
  - env: EXAMPLE_FLAG

tasks:
  - id: c1
    name: add_api_route
    status: todo
  - id: c2
    name: wire_service_logic
    status: todo

tests:
  - id: t1
    command: "pytest tests/test_example.py -q"
    expect: pass
  - id: t2
    command: "curl -sf http://localhost:8000/health"
    expect: pass

exit_criteria:
  - t1
  - t2
```

---

## 7) Operational note for your setup

This method matches your target flow:
- iterate fast in containers on your Mac,
- keep cloud deploy parity,
- then remap providers to your strong hardware later,
without changing acceptance semantics.
