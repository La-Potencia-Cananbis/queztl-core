# SendGrid Setup for senasaitech.com

Microsoft Outlook has disabled basic authentication. We need a proper email service.

## Quick Setup with SendGrid (Free 100 emails/day)

### 1. Create SendGrid Account
- Go to: https://sendgrid.com/
- Sign up (free tier: 100 emails/day forever)
- Verify your email

### 2. Create API Key
- Dashboard → Settings → API Keys
- Click "Create API Key"
- Name: "Queztl Email System"
- Permissions: "Full Access" or "Mail Send"
- Copy the API key (starts with `SG.`)

### 3. Verify Domain (senasaitech.com)
- Dashboard → Settings → Sender Authentication
- Click "Verify a Domain"
- Enter: `senasaitech.com`
- Add DNS records they provide to your domain registrar
- Wait for verification (usually 24-48 hours)

### 4. Create Sender Identity (Quick Start)
While domain verifies, create single sender:
- Dashboard → Settings → Sender Authentication
- Click "Verify a Single Sender"
- Email: `salvador@senasaitech.com`
- From Name: "Salvador Sena"
- Verify the confirmation email

### 5. Update Backend
```bash
export SENDGRID_API_KEY="SG.your-api-key-here"
```

## Alternative: Mailgun (Also Free Tier)
- 5,000 emails/month free
- Same domain verification process
- Even easier API

## Alternative: AWS SES (Production)
- 62,000 emails/month free (first year)
- $0.10 per 1000 emails after
- Requires AWS account
