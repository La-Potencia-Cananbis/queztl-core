#!/bin/bash
# Usage: ./verify_deploy.sh <site-name> <page> <expected>
# Example: ./verify_deploy.sh mysite 3dmark-pro.html "QUEZTL 3DMARK PROFESSIONAL"

SITE="$1"
PAGE="$2"
EXPECTED="$3"

if [ -z "$SITE" ] || [ -z "$PAGE" ] || [ -z "$EXPECTED" ]; then
  echo "Usage: $0 <site-name> <page> <expected-text>"
  exit 1
fi

URL="https://$SITE.netlify.app/$PAGE"

HTML=$(curl -s "$URL")
if echo "$HTML" | grep -q "$EXPECTED"; then
  echo "✅ $PAGE on $SITE: UI change detected ($EXPECTED found)"
  exit 0
else
  echo "❌ $PAGE on $SITE: UI change NOT detected ($EXPECTED not found)"
  exit 2
fi
