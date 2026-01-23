# Mobile Grant Assistant Repo Scaffold Plan (Chat-First PWA)

Purpose: create a dedicated repo for the team-facing, chat-first grant-writing assistant (web + mobile PWA) that talks to Core agents via a gateway API. Neutral, funder-safe; optimized for phones.

## Tech Stack (recommended)
- Frontend: React + Vite + TypeScript, Tailwind for UI. PWA-enabled (manifest + service worker).
- State/query: TanStack Query for API calls + caching; Zustand or React Context for lightweight UI state.
- Forms: React Hook Form + Zod for validation.
- Auth: Email/password with JWT (Auth endpoints on Core Gateway). Client stores access+refresh tokens securely; optional Magic/OTP later.
- Backend API: Existing Core Gateway (FastAPI/HTTP); this repo only consumes it. Stub API client with OpenAPI types if available.
- Build toolchain: pnpm (preferred) or npm; ESLint + Prettier + TypeScript strict.
- Testing: Vitest + Testing Library + Playwright smoke (later); MSW for API mocks.

## Repository layout (proposed)
```
mobile-app/
  apps/
    web/                     # PWA client
      src/
        api/                 # typed API client, hooks
        components/
        features/
          chat/              # chat UI + message store
          sections/          # section drawer & editors
          intake/            # intake wizard
          tracker/           # funder/deadline tracker
          export/            # DOCX/PDF trigger UI
          auth/
        hooks/
        lib/
        pages/
        styles/
        main.tsx
      public/                # icons, manifest, sw registration
      index.html
      vite.config.ts
      tsconfig.json
  packages/
    types/                   # shared TypeScript types (GrantDraft schema, funder, score)
    ui/                      # optional shared UI primitives (buttons, cards, inputs)
  .github/workflows/
    ci.yml                   # lint + test + typecheck
  package.json
  pnpm-workspace.yaml
  tsconfig.base.json
  README.md
```

## Core contracts to respect
- GrantDraft JSON (from chat history): messages[], grant_profile, budget_profile, staffing_profile, sections{}, fundability_score{}, version_snapshots[].
- Core Gateway endpoints (to be aligned):
  - `POST /core/parse_intake`
  - `POST /core/update_section`
  - `POST /core/build_budget`
  - `POST /core/score`
  - `POST /core/export_docx`
- Tone toggle: Neutral / Conservative / Systems-change (no socialist framing in this repo).
- Hard checks: budget totals match target; required sections present; show "what changed" after generations.

## Environment & config
- `.env.example` with `VITE_API_BASE_URL`, `VITE_APP_NAME`, optional Sentry DSN.
- Keep secrets out of repo; use GitHub Encrypted Secrets for CI deploys.

## PWA specifics
- Web app behaves like mobile: single-column layout, large tap targets, offline-ready shell (later enable caching for drafts).
- Add `manifest.webmanifest`, icons, and service worker registration (Vite PWA plugin optional).

## CI/CD
- GitHub Actions `ci.yml`: pnpm install, lint, typecheck, unit tests, build.
- Optional PR previews via Vercel/Netlify (if allowed) or static build artifact.

## Testing strategy
- Unit: pure functions (parsing, mapping chat → sections, score explanations).
- Component: Chat panel, Section drawer, Intake form, Tracker list.
- Integration: happy-path chat → sections → DOCX trigger (mock API with MSW).
- Later: Playwright smoke for mobile viewport.

## Security & guardrails
- Never store tokens in localStorage without refresh rotation; prefer httpOnly if backend allows, otherwise short-lived access + refresh in memory.
- Input validation with Zod; sanitize outputs for display.
- Explicit loading/error states; prevent duplicate submissions.

## Fast start checklist (what to do when creating the repo)
1) Init repo with pnpm workspaces; add `apps/web` with Vite React TS template.
2) Add Tailwind + base design tokens; mobile-first layout.
3) Add auth screens (login, forgot later), protected route shell.
4) Implement Intake form → calls `/core/parse_intake`; store GrantDraft in state.
5) Chat view that updates sections drawer; wire to `/core/update_section`.
6) Score panel from `/core/score` with warnings.
7) Export button hitting `/core/export_docx`.
8) Tracker page for funders/deadlines (local state first, API later).
9) Ship CI (lint/test/typecheck) and README with setup/run steps.

## Follow-ons (post-MVP)
- Version history & diffing of sections.
- Reusable snippet library per org.
- Funder library & cycles with filters.
- Offline drafts + push notifications.
- Capacitor wrap for app stores if needed.
