# AWS Free-Tier Friendly Deployment (Static PWA)

Goal: ship the chat-first PWA to AWS using only free-tier/low-cost services. Backend Core Gateway stays wherever you host it; set `VITE_API_BASE_URL` accordingly.

## Overview
- Build static assets with Vite.
- Host on S3 (static website or private bucket + CloudFront). For lowest friction, use S3 static website; for HTTPS/custom domain, add CloudFront.
- Configure CORS so the frontend can call your Core Gateway.

## Prereqs
- AWS CLI configured (`aws configure`).
- An AWS account within free-tier limits.
- Core Gateway URL reachable over HTTPS (set as `VITE_API_BASE_URL`).

## Build
From `mobile-app/`:
```bash
pnpm install
pnpm build --filter grant-chat-pwa
```
Artifacts land in `apps/web/dist/`.

## Option A: S3 Static Website (fastest)
1) Create bucket (must be globally unique):
```bash
aws s3 mb s3://<your-bucket-name>
```
2) Enable static website hosting and set index:
```bash
aws s3 website s3://<your-bucket-name>/ --index-document index.html
```
3) Upload build:
```bash
aws s3 sync apps/web/dist/ s3://<your-bucket-name>/ --delete
```
4) Make objects publicly readable (for this bucket only):
```bash
aws s3api put-bucket-policy --bucket <your-bucket-name> --policy "$(cat <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::<your-bucket-name>/*"]
    }
  ]
}
EOF
)"
```
5) Find the website URL (HTTP only):
```
http://<your-bucket-name>.s3-website-<region>.amazonaws.com
```
Use for quick demos. For HTTPS/custom domain, add CloudFront (Option B).

## Option B: S3 + CloudFront (HTTPS)
1) Keep the bucket **private**; re-upload the build:
```bash
aws s3 sync apps/web/dist/ s3://<your-bucket-name>/ --delete
```
2) Create a CloudFront distribution with the bucket as origin:
- Origin Access Control (OAC) recommended; allow CloudFront to read the bucket.
- Default root object: `index.html`.
- Viewer protocol policy: Redirect HTTP to HTTPS.
3) Update bucket policy to allow the CloudFront OAC principal.
4) (Optional) Attach a custom domain via Route 53 + ACM certificate in `us-east-1`.
5) Invalidate on deploy:
```bash
aws cloudfront create-invalidation --distribution-id <DIST_ID> --paths "/*"
```

## Environment variable (`VITE_API_BASE_URL`)
- Set at build time: `VITE_API_BASE_URL=https://your-gateway.example.com pnpm build --filter grant-chat-pwa`.
- For S3/CloudFront, the value is baked into the build. For multiple environments, build per env or use a tiny runtime `env.js` pattern.

## CORS (Core Gateway)
Ensure the Core Gateway allows the CloudFront/S3 origin:
- `Access-Control-Allow-Origin: https://<your-domain>` (or `*` for testing)
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

## Minimal deploy script (included)
Use `deploy/deploy-s3.sh`:
```bash
cd mobile-app
VITE_API_BASE_URL=https://your-gateway.example.com \
BUCKET_NAME=<your-bucket> \
DISTRIBUTION_ID=<DIST_ID_optional> \
./deploy/deploy-s3.sh
```

Bucket policies:
- Public static site: `deploy/policies/s3-public-read.json` (replace `REPLACE_BUCKET`).
- CloudFront OAC: `deploy/policies/s3-cloudfront-oac.json` (replace bucket, account, dist ID).

## Costs
- S3 + CloudFront are free/low-cost at small traffic within free-tier. Monitor with AWS Budgets and set alerts.
