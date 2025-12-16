#!/usr/bin/env python3
"""
# QHP Outreach Engine - AI-Powered Investor Outreach Platform
# Like MailChimp, but way better: personalized, intelligent, QHP-powered
"""

# import asyncio
# import json
# import sqlite3
# from datetime import datetime, timedelta
# from typing import Dict, List, Optional, Tuple
# from dataclasses import dataclass, asdict
# from enum import Enum
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from pathlib import Path

# class ContactType(Enum):
#     ANGEL_INVESTOR = "angel_investor"
#     VC_FIRM = "vc_firm"
#     FRIEND_FAMILY = "friend_family"
#     PROFESSIONAL = "professional"
#     CTO = "cto"
#     FOUNDER = "founder"

# class ContactStatus(Enum):
#     NEW = "new"
#     RESEARCHED = "researched"
#     CONTACTED = "contacted"
#     REPLIED = "replied"
#     INTERESTED = "interested"
#     MEETING_SCHEDULED = "meeting_scheduled"
#     PASSED = "passed"
#     INVESTED = "invested"

# class OutreachStage(Enum):
#     COLD_OUTREACH = "cold_outreach"
#     FOLLOW_UP_1 = "follow_up_1"
#     FOLLOW_UP_2 = "follow_up_2"
#     FOLLOW_UP_3 = "follow_up_3"
#     NURTURE = "nurture"
#     CLOSE = "close"

@dataclass
# class Contact:
#     id: str
#     name: str
#     email: str
#     contact_type: ContactType
#     status: ContactStatus
#     company: Optional[str] = None
#     title: Optional[str] = None
#     linkedin: Optional[str] = None
#     twitter: Optional[str] = None
#     investment_history: Optional[str] = None
#     interests: Optional[List[str]] = None
#     tags: Optional[List[str]] = None
#     notes: Optional[str] = None
#     created_at: Optional[str] = None
#     last_contacted: Optional[str] = None
#     next_follow_up: Optional[str] = None
    
#     def __post_init__(self):
#         if self.created_at is None:
#             self.created_at = datetime.now().isoformat()
#         if self.interests is None:
#             self.interests = []
#         if self.tags is None:
#             self.tags = []

@dataclass
# class OutreachEmail:
#     id: str
#     contact_id: str
#     subject: str
#     body: str
#     stage: OutreachStage
#     sent_at: Optional[str] = None
#     opened_at: Optional[str] = None
#     replied_at: Optional[str] = None
#     reply_text: Optional[str] = None
#     personalization_score: float = 0.0

@dataclass
# class Campaign:
#     id: str
#     name: str
#     description: str
#     target_contact_types: List[ContactType]
#     email_templates: Dict[OutreachStage, str]
#     active: bool = True
#     created_at: Optional[str] = None
#     stats: Optional[Dict] = None

# class OutreachEngine:
    """AI-Powered Outreach Engine"""
    
#     def __init__(self, db_path: str = "outreach.db"):
#         self.db_path = db_path
#         self.init_database()
        
#     def init_database(self):
        """Initialize database"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
        # Contacts table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS contacts (
#                 id TEXT PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 email TEXT UNIQUE NOT NULL,
#                 contact_type TEXT NOT NULL,
#                 status TEXT NOT NULL,
#                 company TEXT,
#                 title TEXT,
#                 linkedin TEXT,
#                 twitter TEXT,
#                 investment_history TEXT,
#                 interests TEXT,
#                 tags TEXT,
#                 notes TEXT,
#                 created_at TEXT NOT NULL,
#                 last_contacted TEXT,
#                 next_follow_up TEXT
        """)
        
        # Emails table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS emails (
#                 id TEXT PRIMARY KEY,
#                 contact_id TEXT NOT NULL,
#                 subject TEXT NOT NULL,
#                 body TEXT NOT NULL,
#                 stage TEXT NOT NULL,
#                 sent_at TEXT,
#                 opened_at TEXT,
#                 replied_at TEXT,
#                 reply_text TEXT,
#                 personalization_score REAL,
#                 FOREIGN KEY (contact_id) REFERENCES contacts(id)
        """)
        
        # Campaigns table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS campaigns (
#                 id TEXT PRIMARY KEY,
#                 name TEXT NOT NULL,
#                 description TEXT,
#                 target_contact_types TEXT,
#                 email_templates TEXT,
#                 active INTEGER DEFAULT 1,
#                 created_at TEXT NOT NULL
        """)
        
        # Analytics table
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS analytics (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 event_type TEXT NOT NULL,
#                 contact_id TEXT,
#                 email_id TEXT,
#                 data TEXT
        """)
        
#         conn.commit()
#         conn.close()
    
#     def add_contact(self, contact: Contact) -> Optional[Contact]:
        """Add a new contact"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         try:
#             cursor.execute("""
#                 INSERT INTO contacts 
                (id, name, email, contact_type, status, company, title,
#                  linkedin, twitter, investment_history, interests, tags,
#                  notes, created_at, last_contacted, next_follow_up)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
#                 contact.id, contact.name, contact.email,
#                 contact.contact_type.value, contact.status.value,
#                 contact.company, contact.title, contact.linkedin, contact.twitter,
#                 contact.investment_history,
#                 json.dumps(contact.interests), json.dumps(contact.tags),
#                 contact.notes, contact.created_at,
#                 contact.last_contacted, contact.next_follow_up
            ))
#             conn.commit()
#             self.log_analytics("contact_added", contact.id)
#             return contact
#         except sqlite3.IntegrityError:
#             print(f"  Contact {contact.email} already exists")
#             return None
#         finally:
#             conn.close()
    
#     def get_contacts(self, status: Optional[ContactStatus] = None,
#                      contact_type: Optional[ContactType] = None) -> List[Contact]:
        """Get contacts with filters"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         query = "SELECT * FROM contacts WHERE 1=1"
#         params = []
        
#         if status:
#             query += " AND status = ?"
#             params.append(status.value)
        
#         if contact_type:
#             query += " AND contact_type = ?"
#             params.append(contact_type.value)
        
#         cursor.execute(query, params)
#         rows = cursor.fetchall()
#         conn.close()
        
#         return [self._row_to_contact(row) for row in rows]
    
#     def _row_to_contact(self, row) -> Contact:
        """Convert DB row to Contact"""
#         return Contact(
#             id=row[0], name=row[1], email=row[2],
#             contact_type=ContactType(row[3]), status=ContactStatus(row[4]),
#             company=row[5], title=row[6], linkedin=row[7], twitter=row[8],
#             investment_history=row[9],
#             interests=json.loads(row[10]) if row[10] else [],
#             tags=json.loads(row[11]) if row[11] else [],
#             notes=row[12], created_at=row[13],
#             last_contacted=row[14], next_follow_up=row[15]
    
#     def generate_personalized_email(self, contact: Contact, 
#                                    stage: OutreachStage,
#                                    template: str) -> str:
        """AI-generated personalized email"""
        
        # Build context for AI
#         context = f"""
#         Generate a highly personalized email for:
        
#         Contact: {contact.name}
#         Company: {contact.company or 'N/A'}
#         Title: {contact.title or 'N/A'}
#         Type: {contact.contact_type.value}
#         Interests: {', '.join(contact.interests) if contact.interests else 'N/A'}
#         Investment history: {contact.investment_history or 'N/A'}
        
#         Template to personalize:
        {template}
        
#         Requirements:
        1. Reference their specific background/interests
        2. Keep it conversational and authentic
        3. Clear call-to-action
        4. Under 150 words
        5. Don't sound like a template
        
#         Generate ONLY the email body (no subject line):
        """
        
#         try:
            # Use OpenAI to personalize (or use local model)
            # For now, do intelligent template substitution
#             personalized = template
            
            # Smart replacements
#             personalized = personalized.replace("[NAME]", contact.name.split()[0])
#             personalized = personalized.replace("[FULL_NAME]", contact.name)
#             personalized = personalized.replace("[COMPANY]", contact.company or "your company")
#             personalized = personalized.replace("[TITLE]", contact.title or "your role")
            
            # Add personal touch based on type
#             if contact.contact_type == ContactType.ANGEL_INVESTOR:
#                 if contact.investment_history:
#                     personalized = f"I saw you invested in {contact.investment_history}. " + personalized
#             elif contact.contact_type == ContactType.CTO:
#                 personalized = f"As a technical leader, " + personalized
            
#             return personalized
            
#         except Exception as e:
#             print(f"  AI personalization failed: {e}")
#             return template
    
#     def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create outreach campaign"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             INSERT INTO campaigns
            (id, name, description, target_contact_types, email_templates,
#              active, created_at)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
#             campaign.id, campaign.name, campaign.description,
#             json.dumps([ct.value for ct in campaign.target_contact_types]),
#             json.dumps(campaign.email_templates),
            1 if campaign.active else 0,
#             campaign.created_at or datetime.now().isoformat()
        ))
        
#         conn.commit()
#         conn.close()
#         return campaign
    
#     def send_email(self, contact: Contact, email: OutreachEmail,
#                   smtp_config: Optional[Dict] = None) -> bool:
        """Send email (mock for now)"""
        
#         print(f"\n Sending email to {contact.name} ({contact.email})")
#         print(f"   Subject: {email.subject}")
#         print(f"   Stage: {email.stage.value}")
#         print(f"   Personalization score: {email.personalization_score:.2f}")
        
        # Update contact
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             UPDATE contacts 
#             SET last_contacted = ?, next_follow_up = ?, status = ?
#             WHERE id = ?
        """, (
#             datetime.now().isoformat(),
            (datetime.now() + timedelta(days=3)).isoformat(),
#             ContactStatus.CONTACTED.value,
#             contact.id
        ))
        
        # Save email
#         email.sent_at = datetime.now().isoformat()
#         cursor.execute("""
#             INSERT INTO emails
            (id, contact_id, subject, body, stage, sent_at, personalization_score)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
#             email.id, email.contact_id, email.subject, email.body,
#             email.stage.value, email.sent_at, email.personalization_score
        ))
        
#         conn.commit()
#         conn.close()
        
#         self.log_analytics("email_sent", contact.id, email.id)
        
#         return True
    
#     def run_campaign(self, campaign_id: str, dry_run: bool = True):
        """Execute a campaign"""
        
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
#         row = cursor.fetchone()
#         conn.close()
        
#         if not row:
#             print(f" Campaign {campaign_id} not found")
#             return
        
#         campaign_name = row[1]
#         target_types = [ContactType(t) for t in json.loads(row[3])]
#         templates = json.loads(row[4])
        
#         print(f"\n Running campaign: {campaign_name}")
#         print(f"   Target types: {[t.value for t in target_types]}")
#         print(f"   Dry run: {dry_run}")
        
        # Get eligible contacts
#         eligible = []
#         for contact_type in target_types:
#             contacts = self.get_contacts(
#                 status=ContactStatus.NEW,
#                 contact_type=contact_type
#             eligible.extend(contacts)
        
#         print(f"\n Found {len(eligible)} eligible contacts")
        
        # Send emails
#         sent_count = 0
#         for contact in eligible[:10]:  # Limit to 10 per run
            
            # Generate personalized email
#             template = templates.get("cold_outreach", "")
#             personalized_body = self.generate_personalized_email(
#                 contact, OutreachStage.COLD_OUTREACH, template
            
#             email = OutreachEmail(
#                 id=f"email_{contact.id}_{datetime.now().timestamp()}",
#                 contact_id=contact.id,
#                 subject=f"QHP Protocol - {contact.name}",
#                 body=personalized_body,
#                 stage=OutreachStage.COLD_OUTREACH,
#                 personalization_score=0.85
            
#             if not dry_run:
#                 self.send_email(contact, email)
#                 sent_count += 1
#             else:
#                 print(f"\n   Would send to: {contact.name} ({contact.email})")
#                 print(f"   Preview: {personalized_body[:100]}...")
        
#         print(f"\n Campaign complete: {sent_count} emails sent")
    
#     def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
        # Total contacts
#         cursor.execute("SELECT COUNT(*) FROM contacts")
#         total_contacts = cursor.fetchone()[0]
        
        # By status
#         cursor.execute("""
#             SELECT status, COUNT(*) 
#             FROM contacts 
#             GROUP BY status
        """)
#         by_status = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Emails sent
#         cursor.execute("SELECT COUNT(*) FROM emails WHERE sent_at IS NOT NULL")
#         emails_sent = cursor.fetchone()[0]
        
        # Reply rate
#         cursor.execute("SELECT COUNT(*) FROM emails WHERE replied_at IS NOT NULL")
#         replies = cursor.fetchone()[0]
#         reply_rate = (replies / emails_sent * 100) if emails_sent > 0 else 0
        
        # Interested contacts
#         cursor.execute("""
#             SELECT COUNT(*) FROM contacts 
#             WHERE status IN ('interested', 'meeting_scheduled', 'invested')
        """)
#         interested = cursor.fetchone()[0]
        
#         conn.close()
        
#         return {
            "total_contacts": total_contacts,
            "by_status": by_status,
            "emails_sent": emails_sent,
            "replies": replies,
            "reply_rate": f"{reply_rate:.1f}%",
            "interested": interested,
            "conversion_rate": f"{(interested / total_contacts * 100):.1f}%" if total_contacts > 0 else "0%"
        }
    
#     def log_analytics(self, event_type: str, contact_id: Optional[str] = None, 
#                      email_id: Optional[str] = None, data: Optional[Dict] = None):
        """Log analytics event"""
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             INSERT INTO analytics (timestamp, event_type, contact_id, email_id, data)
#             VALUES (?, ?, ?, ?, ?)
        """, (
#             datetime.now().isoformat(), event_type, contact_id, email_id,
#             json.dumps(data) if data else None
        ))
        
#         conn.commit()
#         conn.close()
    
#     def suggest_next_actions(self) -> List[Dict]:
        """AI suggests what to do next"""
#         actions = []
        
        # Check for follow-ups needed
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
        
#         cursor.execute("""
#             SELECT id, name, email, next_follow_up
#             FROM contacts
#             WHERE next_follow_up <= ? AND status = 'contacted'
#             ORDER BY next_follow_up ASC
#             LIMIT 5
        """, (datetime.now().isoformat(),))
        
#         follow_ups = cursor.fetchall()
#         for row in follow_ups:
#             actions.append({
                "type": "follow_up",
                "priority": "high",
                "contact_id": row[0],
                "contact_name": row[1],
                "action": f"Send follow-up to {row[1]} ({row[2]})"
            })
        
        # Check for new contacts to reach out to
#         cursor.execute("""
#             SELECT COUNT(*) FROM contacts WHERE status = 'new'
        """)
#         new_contacts = cursor.fetchone()[0]
        
#         if new_contacts > 0:
#             actions.append({
                "type": "initial_outreach",
                "priority": "medium",
                "count": new_contacts,
                "action": f"Reach out to {new_contacts} new contacts"
            })
        
#         conn.close()
        
#         return actions

# def load_investor_contacts(engine: OutreachEngine):
    """Load sample investor contacts"""
    
#     print(" Loading investor contacts...")
    
    # Angel investors
#     angels = [
#         Contact(
#             id="angel_001",
#             name="Sarah Chen",
#             email="sarah@techventures.com",
#             contact_type=ContactType.ANGEL_INVESTOR,
#             status=ContactStatus.NEW,
#             company="Tech Ventures",
#             title="Angel Investor",
#             linkedin="linkedin.com/in/sarahchen",
#             investment_history="Stripe, Vercel, Supabase",
#             interests=["dev tools", "infrastructure", "open source"],
#             tags=["high-priority", "dev-tools-focus"]
        ),
#         Contact(
#             id="angel_002",
#             name="Marcus Williams",
#             email="marcus@devangels.io",
#             contact_type=ContactType.ANGEL_INVESTOR,
#             status=ContactStatus.NEW,
#             company="DevAngels",
#             title="Managing Partner",
#             linkedin="linkedin.com/in/marcuswilliams",
#             investment_history="Twilio, SendGrid, Kong",
#             interests=["APIs", "developer platforms", "SaaS"],
#             tags=["high-priority", "api-focus"]
        ),
    ]
    
    # Friends & Family
#     friends = [
#         Contact(
#             id="friend_001",
#             name="Alex Rodriguez",
#             email="alex@example.com",
#             contact_type=ContactType.FRIEND_FAMILY,
#             status=ContactStatus.NEW,
#             notes="Former colleague, expressed interest in investing",
#             tags=["warm-intro", "small-check"]
        ),
    ]
    
    # CTOs for pre-selling
#     ctos = [
#         Contact(
#             id="cto_001",
#             name="Jennifer Park",
#             email="jennifer@techcorp.com",
#             contact_type=ContactType.CTO,
#             status=ContactStatus.NEW,
#             company="TechCorp",
#             title="CTO",
#             linkedin="linkedin.com/in/jenniferpark",
#             interests=["microservices", "performance", "cloud-native"],
#             tags=["enterprise", "hot-lead"]
        ),
    ]
    
#     for contact in angels + friends + ctos:
#         engine.add_contact(contact)
    
#     print(f" Loaded {len(angels + friends + ctos)} contacts")

# def create_investor_campaign(engine: OutreachEngine):
    """Create investor outreach campaign"""
    
#     campaign = Campaign(
#         id="campaign_investor_001",
#         name="Seed Round Investor Outreach",
#         description="Cold outreach to angel investors for $25K-$100K seed round",
#         target_contact_types=[ContactType.ANGEL_INVESTOR, ContactType.VC_FIRM],
#         email_templates={
#             OutreachStage.COLD_OUTREACH.value: """Hi [NAME],

# I'm building QHP - a protocol that's 10-20x faster than REST APIs. We've coined "Quantized Action Packets" (QAPs) - the world's first port-free protocol.

# I noticed you invested in [INVESTMENT_HISTORY]. QHP is similar infrastructure - foundational layer that developers will adopt organically.

# We're raising $25K-$100K to:
#  File patents/trademarks ($900)
#  Get first 10 enterprise customers
 6 months runway

# Working implementation, proven 10-20x performance, clear path to $250K ARR.

# Would you have 15 minutes for a quick call this week?

# Best,
[YOUR_NAME]""",
#             OutreachStage.FOLLOW_UP_1.value: """Hi [NAME],

# Following up on my email about QHP protocol. 

# Quick update: We just filed our provisional patent and are seeing strong interest from 3 enterprise prospects.

# Still looking for $25K-$50K to close this round.

# Are you interested in learning more?

# Best,
[YOUR_NAME]""",
        }
    
#     engine.create_campaign(campaign)
#     print(f" Created campaign: {campaign.name}")
    
#     return campaign

# if __name__ == "__main__":
#     print("="*60)
#     print(" QHP OUTREACH ENGINE - Better than MailChimp!")
#     print("="*60)
    
    # Initialize
#     engine = OutreachEngine()
    
    # Load contacts
#     load_investor_contacts(engine)
    
    # Create campaign
#     campaign = create_investor_campaign(engine)
    
    # Show dashboard
#     print("\n" + "="*60)
#     print(" DASHBOARD")
#     print("="*60)
    
#     stats = engine.get_dashboard_stats()
#     print(f"\nContacts: {stats['total_contacts']}")
#     print(f"Emails sent: {stats['emails_sent']}")
#     print(f"Reply rate: {stats['reply_rate']}")
#     print(f"Interested: {stats['interested']}")
#     print(f"Conversion: {stats['conversion_rate']}")
    
#     print(f"\nBy status:")
#     for status, count in stats['by_status'].items():
#         print(f"  {status}: {count}")
    
    # Suggest actions
#     print("\n" + "="*60)
#     print(" AI RECOMMENDATIONS")
#     print("="*60)
    
#     actions = engine.suggest_next_actions()
#     for i, action in enumerate(actions, 1):
#         print(f"\n{i}. [{action['priority'].upper()}] {action['action']}")
    
    # Run campaign (dry run)
#     print("\n" + "="*60)
#     print(" CAMPAIGN DRY RUN")
#     print("="*60)
    
#     engine.run_campaign(campaign.id, dry_run=True)
    
#     print("\n Outreach engine ready!")
#     print("\nNext steps:")
#     print("1. Add your real contacts")
#     print("2. Configure SMTP settings")
#     print("3. Run campaign with dry_run=False")
#     print("4. Track responses and conversions")
