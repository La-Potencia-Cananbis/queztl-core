# Quick SMTP Setup for Real Email Sending

## Problem
Your emails are being stored in the backend but not actually sent to recipients' real email addresses.

## Solution Options

### Option 1: Use Your Live.com Email (Simplest)

1. **Get an App Password from Microsoft**:
   - Go to: https://account.live.com/proofs/manage/additional
   - Click "Create a new app password"
   - Copy the generated password

2. **Set Environment Variable**:
   ```bash
   export SMTP_PASSWORD="your-app-password-here"
   ```

3. **Restart Backend**:
   ```bash
   ./start-email-backend.sh
   ```

Now emails will actually be sent from salvadorsena@live.com!

### Option 2: Use SendGrid (Professional)

1. **Sign up**: https://signup.sendgrid.com/
2. **Get API Key**: Settings → API Keys
3. **Update backend to use SendGrid API**

### Option 3: Use AWS SES (Scalable)

1. **Sign up for AWS**: https://aws.amazon.com/ses/
2. **Verify your domain**: senasaitech.com
3. **Get SMTP credentials**
4. **Update env vars**

## Quick Test

After setting SMTP_PASSWORD:

```bash
# Restart backend with SMTP
export SMTP_PASSWORD="your-app-password"
.venv/bin/python backend/email_service.py

# Send test email
curl -X POST http://localhost:8001/api/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "salvador@senasaitech.app",
    "recipients": ["msilvab@gmail.com"],
    "subject": "Test from Queztl",
    "body": "This is a real email sent via SMTP!",
    "encrypt": true
  }'
```

## Current Status

✅ Backend updated to support real SMTP
✅ Configured to use salvadorsena@live.com
⚠️ Needs SMTP_PASSWORD environment variable to work

## Next Step

**Get your Microsoft App Password now:**
https://account.live.com/proofs/manage/additional

Then restart the backend with:
```bash
export SMTP_PASSWORD="your-app-password"
./start-email-backend.sh
```

Your emails will then be delivered for real! 🚀
