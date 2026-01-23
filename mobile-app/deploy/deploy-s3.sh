#!/usr/bin/env bash
set -euo pipefail

# Deploy static PWA to S3 (optionally with CloudFront invalidation)
# Usage:
#   VITE_API_BASE_URL=https://your-gateway.example.com \
#   BUCKET_NAME=your-bucket-name \
#   DISTRIBUTION_ID=E1234567890 (optional) \
#   ./deploy/deploy-s3.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/apps/web"
DIST_DIR="$APP_DIR/dist"

: "${BUCKET_NAME:?Set BUCKET_NAME}" 
VITE_API_BASE_URL="${VITE_API_BASE_URL:-}" 
DISTRIBUTION_ID="${DISTRIBUTION_ID:-}" 

cd "$ROOT_DIR"

if [[ -z "$VITE_API_BASE_URL" ]]; then
  echo "[warn] VITE_API_BASE_URL not set; build will use mock backend." >&2
fi

echo "[build] Building app with VITE_API_BASE_URL=${VITE_API_BASE_URL:-'(mock)'}"
VITE_API_BASE_URL="$VITE_API_BASE_URL" pnpm build --filter grant-chat-pwa

echo "[sync] Uploading dist to s3://$BUCKET_NAME/"
aws s3 sync "$DIST_DIR/" "s3://$BUCKET_NAME/" --delete

echo "[verify] Listing bucket root (first 5 objects)"
aws s3 ls "s3://$BUCKET_NAME/" | head -n 5

if [[ -n "$DISTRIBUTION_ID" ]]; then
  echo "[cf] Creating CloudFront invalidation for /*"
  aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths "/*"
fi

echo "[done] Deploy complete."