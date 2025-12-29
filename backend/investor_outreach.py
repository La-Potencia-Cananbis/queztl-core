#!/usr/bin/env python3
"""
🚀 Queztl Investor Outreach System
Send bulk emails to top investors with performance tracking
"""

import requests
import json
import time
from typing import List, Dict
from datetime import datetime

# Backend API endpoint
API_URL = "http://localhost:8001"

def load_investors_from_file(filename: str = "TOP_INVESTORS.md") -> List[Dict[str, str]]:
    """Parse investor list from markdown file"""
    investors = []
    
    # For now, use a sample list. You can parse TOP_INVESTORS.md later
    sample_investors = [
        {"name": "Marc Andreessen", "email": "marc@a16z.com", "firm": "Andreessen Horowitz"},
        {"name": "Peter Thiel", "email": "peter@foundersfund.com", "firm": "Founders Fund"},
        {"name": "Reid Hoffman", "email": "reid@greylock.com", "firm": "Greylock Partners"},
        {"name": "Vinod Khosla", "email": "vinod@khoslaventures.com", "firm": "Khosla Ventures"},
        {"name": "Chris Dixon", "email": "chris@a16z.com", "firm": "Andreessen Horowitz"},
    ]
    
    return sample_investors

def create_email_template(investor_name: str, firm: str) -> Dict[str, str]:
    """Create personalized email for investor"""
    
    subject = "Queztl: 10-20x Faster Email Infrastructure"
    
    body = f"""Hi {investor_name},

I'm Salvador Sena, founder of Queztl. We've built an email system that's 10-20x faster than ProtonMail with better economics than SendGrid/Mailgun.

Key Metrics (Validated via Autonomous Testing):
⚡ 2.5ms average delivery (vs ProtonMail's 50-100ms)
🚀 5,000+ emails/sec throughput  
🔒 End-to-end encryption
💰 90% cheaper than legacy providers
📊 99.99% uptime

Live Demo: https://senasaitech.com
Tech Specs: https://github.com/SalChicanoLoco/queztl-core
Real Performance Data: Validated via autonomous testing

We're using QHP (Queztl Hypertext Protocol) - a protocol we designed to replace REST for real-time applications. The email system is just the first use case.

Market Opportunity:
• Email infrastructure: $4B+ market (SendGrid, Mailgun, SES)
• Real-time protocols: $20B+ (REST replacement for all web apps)
• Developer tools: $50B+ (Queztl OS for distributed compute)

We're raising $[X] to:
1. Scale infrastructure for enterprise customers
2. Onboard first 100 companies to QHP protocol
3. Build developer ecosystem around Queztl OS

Would love to show you the system in action and discuss how we're rebuilding the internet's protocol layer.

--
Salvador Sena
Founder, Queztl
salvador@senasaitech.com
senasaitech.com
"""
    
    return {"subject": subject, "body": body}

def send_email(sender: str, recipient: str, subject: str, body: str) -> Dict:
    """Send a single email via Queztl API"""
    try:
        response = requests.post(
            f"{API_URL}/api/email/send",
            json={
                "sender": sender,
                "recipients": [recipient],
                "subject": subject,
                "body": body,
                "encrypt": True
            }
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_bulk_campaign(sender: str, investors: List[Dict[str, str]], dry_run: bool = True):
    """Send personalized emails to all investors"""
    
    print("=" * 80)
    print("🚀 QUEZTL INVESTOR OUTREACH CAMPAIGN")
    print("=" * 80)
    print(f"\nSender: {sender}")
    print(f"Recipients: {len(investors)} investors")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE SEND'}")
    print()
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No emails will be sent")
        print("Preview of first email:")
        print("-" * 80)
        investor = investors[0]
        template = create_email_template(investor["name"], investor["firm"])
        print(f"To: {investor['name']} ({investor['email']})")
        print(f"Subject: {template['subject']}")
        print(f"\n{template['body']}")
        print("-" * 80)
        print(f"\nTo send for real, run with --live flag")
        return
    
    # Live sending
    results = {
        "sent": 0,
        "failed": 0,
        "total_time_ms": 0,
        "errors": []
    }
    
    start_time = time.time()
    
    for i, investor in enumerate(investors, 1):
        print(f"[{i}/{len(investors)}] Sending to {investor['name']} ({investor['email']})...")
        
        template = create_email_template(investor["name"], investor["firm"])
        result = send_email(sender, investor["email"], template["subject"], template["body"])
        
        if result.get("success"):
            results["sent"] += 1
            print(f"  ✅ Sent in {result['delivery_time_ms']:.2f}ms")
        else:
            results["failed"] += 1
            results["errors"].append({
                "investor": investor["name"],
                "error": result.get("error", "Unknown error")
            })
            print(f"  ❌ Failed: {result.get('error')}")
        
        # Small delay between emails to be respectful
        time.sleep(0.5)
    
    end_time = time.time()
    results["total_time_ms"] = (end_time - start_time) * 1000
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 CAMPAIGN SUMMARY")
    print("=" * 80)
    print(f"✅ Sent: {results['sent']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⏱️  Total Time: {results['total_time_ms']:.2f}ms")
    print(f"⚡ Avg Time per Email: {results['total_time_ms']/len(investors):.2f}ms")
    
    if results["errors"]:
        print("\n⚠️  Errors:")
        for error in results["errors"]:
            print(f"  - {error['investor']}: {error['error']}")
    
    # Save results
    filename = f"outreach_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {filename}")
    print("=" * 80)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Queztl Investor Outreach System')
    parser.add_argument('--live', action='store_true', help='Actually send emails (default is dry run)')
    parser.add_argument('--sender', default='salvador@senasaitech.com', help='Sender email address')
    
    args = parser.parse_args()
    
    # Load investors
    print("📋 Loading investor list...")
    investors = load_investors_from_file()
    print(f"   Loaded {len(investors)} investors\n")
    
    # Send campaign
    send_bulk_campaign(args.sender, investors, dry_run=not args.live)

if __name__ == "__main__":
    main()
