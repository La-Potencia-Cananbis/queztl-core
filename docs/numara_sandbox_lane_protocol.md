# NUMARA Sandbox Lane Protocol

Status: canonical operating note

Purpose: define how experimental NUMARA artifacts are added without contaminating core runtime, agent, router, or production-memory structures.

## What happened

A self-contained interactive demo was added under:

```text
demos/numara-chimayo-substrate/
  index.html
  README.md
  numara-seed.json
```

The first file, `index.html`, was created directly on `main` in commit:

```text
37f173031ec05c9b58bfe98ad850f8eea83e78f4
```

That was procedurally non-ideal. It did not modify existing runtime files, but it bypassed the preferred PR lane.

A follow-up PR added the artifact metadata:

```text
PR #16: Add NUMARA Chimayo substrate artifact
Merge commit: ac2931aa4944ae2471417638114b0049b57506a2
```

## Containment result

The artifact is contained to the `demos/` directory.

No changes were made to:

```text
core runtime
agent runtime
router/API code
FastAPI services
Ray workers
Python modules
existing production docs
existing NUMARA core files
```

Airtable records were written only to:

```text
Base: NUMARA — Session State
Table: SESSION_SPINE
```

No records were written to:

```text
Symbolic Kernel Sandbox
Projects
Research
Pipeline
```

## Canonical rule going forward

All experimental NUMARA artifacts must use a sandbox lane.

```text
main
  <- PR only
feature/* or docs/*
  <- all new work
```

No direct writes to `main` unless explicitly requested by the human operator.

## Directory contract

Experimental artifacts live under:

```text
demos/<artifact-name>/
```

A complete artifact should include:

```text
index.html          # runnable static demo, if applicable
README.md           # purpose, architecture, validation
numara-seed.json    # graph seed / substrate payload
```

Optional files:

```text
PR_BODY.md
VALIDATION.md
CHANGELOG.md
```

## Airtable contract

Session-state artifacts must be logged to:

```text
Base: NUMARA — Session State
Table: SESSION_SPINE
```

Required record pattern:

```text
artifact_id     stable identifier
 type           graph | node | edge | rule | runtime | artifact | deploy | note
 stage          seed | semantic | runtime | github | merged | packaged
 content        full payload or structured note
 summary        short human-readable summary
 dependencies   comma-separated dependency IDs
 confidence     low | medium | high
```

Experimental graph records should not be written to production-facing project tables unless explicitly promoted.

## Promotion rule

An artifact may move from sandbox to core only after:

1. Human review of diff.
2. Validation checklist completed.
3. Explicit promotion PR opened.
4. Airtable SESSION_SPINE updated with promotion record.
5. No direct merge into runtime-critical paths.

## Validation checklist

Before merge:

```text
[ ] Artifact is under demos/<artifact-name>/ or docs/
[ ] Existing runtime files untouched
[ ] No secrets or tokens included
[ ] No external API keys embedded
[ ] Static files open locally
[ ] README explains purpose and boundary
[ ] numara-seed.json is valid JSON if included
[ ] Airtable record points to sandbox lane
[ ] PR is reviewed before merge
```

## Recovery note for Chimayo artifact

The Chimayo substrate artifact is accepted as a sandbox artifact because its files are isolated under:

```text
demos/numara-chimayo-substrate/
```

The direct `main` commit should be treated as an exception, not precedent.

Canonical posture:

```text
safe to keep
not core runtime
not production brain
sandbox lane artifact
```

## Short version

```text
If it is experimental, put it in demos/.
If AI writes it, use a branch and PR.
If it is memory, log it in SESSION_SPINE.
If it touches core, stop and review first.
```
