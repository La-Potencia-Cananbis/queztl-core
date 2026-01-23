# Mobile Grant Chat Assistant (PWA) — Scaffold

Chat-first web + mobile PWA for team grant drafting, consuming Core Gateway APIs. Neutral, funder-safe, phone-friendly.

## What’s here
- pnpm workspace with `apps/web` (React + Vite + TS) and shared `packages/types`.
- Minimal UI shell (chat placeholder, sections/fundability placeholders) and PWA manifest.
- Base TypeScript config, ESLint scripts, and workspace wiring.

## Quick start
```bash
cd mobile-app
pnpm install
pnpm dev --filter grant-chat-pwa
```
Then open the printed local URL (defaults to http://localhost:5173).

### AWS free-tier deploy (static hosting)
See `deploy/aws-free-tier.md` for S3/CloudFront steps. Build with your API endpoint baked in:
```bash
VITE_API_BASE_URL=https://your-gateway.example.com pnpm build --filter grant-chat-pwa
aws s3 sync apps/web/dist/ s3://<your-bucket>/ --delete
```
Add CloudFront for HTTPS/custom domain.

## Next steps (build plan)
1) Wire auth + API base URL via `.env` (`VITE_API_BASE_URL`). If unset, the app uses a local mock generator so you can demo without backend.
2) Implement Core Gateway calls: parse_intake, update_section, build_budget, score, export_docx.
3) Replace placeholder chat with real message store → section snapshots. (Done: chat shell + mock fallback.)
4) Add fundability panel + warnings; enforce required-section checks. (Scaffolded with mock score.)
5) Hook export to backend DOCX generation; add tracker view for deadlines.

## Notes
- Keep tokens short-lived; prefer httpOnly cookies if backend allows. Otherwise, store access in memory and refresh securely.
- Add CI (lint/typecheck/test/build) when the API contracts are stable.
- For mobile feel, keep layouts single-column with large tap targets; consider Vite PWA plugin + offline caching later.
