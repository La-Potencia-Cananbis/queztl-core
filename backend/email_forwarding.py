#!/usr/bin/env python3
"""
# Email Forwarding Configuration for QuetzalCore Email
# Forward all emails to salvadorsena@live.com until desktop app is ready
"""

# FORWARDING_RULES = {
    "salvador@senasaitech.app": "salvadorsena@live.com",
    "founder@senasaitech.app": "salvadorsena@live.com",
    # Add more forwarding rules as needed
}

# def should_forward(recipient: str) -> bool:
    """Check if email should be forwarded"""
#     return recipient in FORWARDING_RULES

# def get_forward_address(recipient: str) -> str:
    """Get the forwarding address for a recipient"""
#     return FORWARDING_RULES.get(recipient, "")

# Configuration for SMTP forwarding (when connected to real mail server)
# SMTP_CONFIG = {
    "host": "smtp.live.com",  # Outlook/Live.com SMTP
    "port": 587,
    "use_tls": True,
    "username": "salvadorsena@live.com",  # Set this in production
    "password": "",  # Set via environment variable
}
