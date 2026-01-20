#!/usr/bin/env python3
"""
Contact Form API - Handle form submissions, send emails, store in DB
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import json

app = FastAPI(title="Contact Form API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = Path("data/members.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            message TEXT,
            member_type TEXT DEFAULT 'recruit',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            contacted BOOLEAN DEFAULT FALSE
        )
    """)
    
    conn.commit()
    conn.close()

init_db()

# Models
class ContactSubmission(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""
    message: str
    member_type: str = "recruit"  # recruit, member, supporter

class EmailConfig(BaseModel):
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = "queztl@example.com"  # Replace with real
    sender_password: str = ""  # Use environment variable
    recipient_email: str = "admin@example.com"  # Replace with real

# Email configuration (load from env or config file)
EMAIL_CONFIG = EmailConfig()

def send_email_notification(submission: ContactSubmission):
    """Send email notification"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG.sender_email
        msg['To'] = EMAIL_CONFIG.recipient_email
        msg['Subject'] = f"New Contact Form Submission - {submission.name}"
        
        body = f"""
New contact form submission received:

Name: {submission.name}
Email: {submission.email}
Phone: {submission.phone}
Type: {submission.member_type}

Message:
{submission.message}

Submitted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        if EMAIL_CONFIG.sender_password:  # Only send if configured
            server = smtplib.SMTP(EMAIL_CONFIG.smtp_server, EMAIL_CONFIG.smtp_port)
            server.starttls()
            server.login(EMAIL_CONFIG.sender_email, EMAIL_CONFIG.sender_password)
            server.send_message(msg)
            server.quit()
            return True
        else:
            print("⚠️  Email not configured - skipping send")
            return False
            
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def save_to_database(submission: ContactSubmission):
    """Save submission to database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO members (name, email, phone, message, member_type)
            VALUES (?, ?, ?, ?, ?)
        """, (
            submission.name,
            submission.email,
            submission.phone,
            submission.message,
            submission.member_type
        ))
        
        conn.commit()
        member_id = cursor.lastrowid
        conn.close()
        
        return member_id
        
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/submit")
async def submit_contact_form(submission: ContactSubmission):
    """Handle contact form submission"""
    
    # Save to database
    member_id = save_to_database(submission)
    
    # Send email notification
    email_sent = send_email_notification(submission)
    
    return {
        "success": True,
        "message": "Thank you! Your submission has been received.",
        "member_id": member_id,
        "email_sent": email_sent
    }

@app.get("/members")
async def get_members():
    """Get all members (admin endpoint)"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM members ORDER BY submitted_at DESC")
    members = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return members

@app.get("/stats")
async def get_stats():
    """Get member statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM members")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM members WHERE member_type = 'member'")
    members = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM members WHERE member_type = 'recruit'")
    recruits = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM members WHERE contacted = FALSE")
    pending = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "members": members,
        "recruits": recruits,
        "pending_contact": pending
    }

@app.patch("/members/{member_id}/contacted")
async def mark_contacted(member_id: int):
    """Mark member as contacted"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE members SET contacted = TRUE WHERE id = ?", (member_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Member not found")
    
    conn.close()
    return {"success": True}

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "service": "contact_form_api",
        "database": str(DB_PATH),
        "email_configured": bool(EMAIL_CONFIG.sender_password)
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Contact Form API on http://localhost:8003")
    uvicorn.run(app, host="0.0.0.0", port=8003)
