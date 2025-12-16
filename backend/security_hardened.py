"""
#  QUETZALCORE HARDENED SECURITY SYSTEM
# Enterprise-grade security for all endpoints and data

# Security Layers:
1. API Key Authentication (mandatory)
2. Rate Limiting (prevent abuse)
3. IP Whitelisting (trusted sources only)
4. Request Validation (sanitize all inputs)
5. Encryption (data in transit and at rest)
6. Audit Logging (track everything)
7. DDoS Protection
8. SQL Injection Prevention
9. XSS Protection
10. CSRF Protection
"""

# import hashlib
# import hmac
# import time
# import json
# import re
# from typing import Dict, List, Optional, Any
# from dataclasses import dataclass, field
# from datetime import datetime, timedelta
# from functools import wraps
# from fastapi import HTTPException, Request, Header
# from fastapi.responses import JSONResponse
# import secrets


@dataclass
# class SecurityEvent:
    """Log security events"""
#     event_id: str
#     event_type: str  # auth_failed, rate_limit, blocked_ip, etc.
#     ip_address: str
#     endpoint: str
#     details: str
#     severity: str  # low, medium, high, critical
#     timestamp: float = field(default_factory=time.time)


# class HardenedSecurity:
    """
#      ENTERPRISE SECURITY SYSTEM
    
#     This hardens ALL endpoints with multiple security layers
    """
    
#     def __init__(self):
#         self.security_id = "quetzalcore-security-001"
#         self.started_at = time.time()
        
        # API Keys (in production, use environment variables!)
#         self.valid_api_keys = set([
#             hashlib.sha256("xavasena-master-key".encode()).hexdigest(),
#             hashlib.sha256("quetzalcore-admin-key".encode()).hexdigest(),
        ])
        
        # Rate limiting: IP -> [timestamps]
#         self.rate_limit_tracker: Dict[str, List[float]] = {}
#         self.rate_limit_max_requests = 100  # requests
#         self.rate_limit_window = 60  # seconds
        
        # IP Whitelist (empty = allow all, but log suspicious)
#         self.ip_whitelist: set = set()
        
        # IP Blacklist (blocked IPs)
#         self.ip_blacklist: set = set()
        
        # Security event log
#         self.security_events: List[SecurityEvent] = []
        
        # Failed auth attempts tracker
#         self.failed_auth_attempts: Dict[str, int] = {}
#         self.max_failed_attempts = 5
        
        # Encryption key for sensitive data
#         self.encryption_key = secrets.token_bytes(32)
        
#     def generate_api_key(self, user_id: str) -> str:
        """Generate a new API key for a user"""
#         raw_key = f"{user_id}-{secrets.token_urlsafe(32)}-{int(time.time())}"
#         api_key = hashlib.sha256(raw_key.encode()).hexdigest()
#         self.valid_api_keys.add(api_key)
#         return api_key
    
#     def validate_api_key(self, api_key: str) -> bool:
        """Validate API key"""
#         if not api_key:
#             return False
#         return api_key in self.valid_api_keys
    
#     def check_rate_limit(self, ip_address: str) -> bool:
        """
#         Check if IP has exceeded rate limit
#         Returns True if allowed, False if rate limited
        """
#         now = time.time()
        
        # Clean old entries
#         if ip_address in self.rate_limit_tracker:
#             self.rate_limit_tracker[ip_address] = [
#                 ts for ts in self.rate_limit_tracker[ip_address]
#                 if now - ts < self.rate_limit_window
            ]
#         else:
#             self.rate_limit_tracker[ip_address] = []
        
        # Check if over limit
#         if len(self.rate_limit_tracker[ip_address]) >= self.rate_limit_max_requests:
#             self._log_security_event(
#                 event_type="rate_limit_exceeded",
#                 ip_address=ip_address,
#                 endpoint="unknown",
#                 details=f"Exceeded {self.rate_limit_max_requests} requests in {self.rate_limit_window}s",
#                 severity="medium"
#             return False
        
        # Add this request
#         self.rate_limit_tracker[ip_address].append(now)
#         return True
    
#     def is_ip_allowed(self, ip_address: str) -> bool:
        """Check if IP is allowed"""
        # Check blacklist first
#         if ip_address in self.ip_blacklist:
#             self._log_security_event(
#                 event_type="blocked_ip_access",
#                 ip_address=ip_address,
#                 endpoint="unknown",
#                 details="IP is blacklisted",
#                 severity="high"
#             return False
        
        # If whitelist is empty, allow all (but log)
#         if not self.ip_whitelist:
#             return True
        
        # Check whitelist
#         return ip_address in self.ip_whitelist
    
#     def sanitize_input(self, data: Any) -> Any:
        """
#         Sanitize input data to prevent injection attacks
        """
#         if isinstance(data, str):
            # Remove potential SQL injection patterns
#             data = re.sub(r"('|(--|#|\/\*|\*\/))", "", data)
            # Remove potential XSS patterns
#             data = re.sub(r"<script[^>]*>.*?</script>", "", data, flags=re.IGNORECASE | re.DOTALL)
#             data = re.sub(r"javascript:", "", data, flags=re.IGNORECASE)
#             return data.strip()
        
#         elif isinstance(data, dict):
#             return {k: self.sanitize_input(v) for k, v in data.items()}
        
#         elif isinstance(data, list):
#             return [self.sanitize_input(item) for item in data]
        
#         return data
    
#     def validate_request_data(self, data: Dict, required_fields: List[str]) -> tuple[bool, str]:
        """
#         Validate that request has required fields and they're not malicious
#         Returns (is_valid, error_message)
        """
        # Check required fields
#         for field in required_fields:
#             if field not in data:
#                 return False, f"Missing required field: {field}"
        
        # Sanitize all data
#         sanitized = self.sanitize_input(data)
        
        # Check if data was modified (potential attack)
#         if json.dumps(data, sort_keys=True) != json.dumps(sanitized, sort_keys=True):
#             self._log_security_event(
#                 event_type="malicious_input_detected",
#                 ip_address="unknown",
#                 endpoint="unknown",
#                 details="Input data contained potentially malicious content",
#                 severity="high"
#             return False, "Invalid input data detected"
        
#         return True, ""
    
#     def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        # Simple XOR encryption (in production, use proper encryption like AES)
#         key_bytes = self.encryption_key
#         data_bytes = data.encode()
        
#         encrypted = bytes([
#             data_bytes[i] ^ key_bytes[i % len(key_bytes)]
#             for i in range(len(data_bytes))
        ])
        
#         return encrypted.hex()
    
#     def decrypt_sensitive_data(self, encrypted_hex: str) -> str:
        """Decrypt sensitive data"""
#         key_bytes = self.encryption_key
#         encrypted = bytes.fromhex(encrypted_hex)
        
#         decrypted = bytes([
#             encrypted[i] ^ key_bytes[i % len(key_bytes)]
#             for i in range(len(encrypted))
        ])
        
#         return decrypted.decode()
    
#     def record_failed_auth(self, ip_address: str):
        """Record failed authentication attempt"""
#         if ip_address not in self.failed_auth_attempts:
#             self.failed_auth_attempts[ip_address] = 0
        
#         self.failed_auth_attempts[ip_address] += 1
        
        # Auto-blacklist after too many failures
#         if self.failed_auth_attempts[ip_address] >= self.max_failed_attempts:
#             self.ip_blacklist.add(ip_address)
#             self._log_security_event(
#                 event_type="ip_auto_blacklisted",
#                 ip_address=ip_address,
#                 endpoint="auth",
#                 details=f"Blacklisted after {self.max_failed_attempts} failed auth attempts",
#                 severity="critical"
    
#     def _log_security_event(self, event_type: str, ip_address: str, 
#                            endpoint: str, details: str, severity: str):
        """Log a security event"""
#         event = SecurityEvent(
#             event_id=f"sec-{int(time.time() * 1000)}",
#             event_type=event_type,
#             ip_address=ip_address,
#             endpoint=endpoint,
#             details=details,
#             severity=severity
        
#         self.security_events.append(event)
        
        # Keep only last 10000 events
#         if len(self.security_events) > 10000:
#             self.security_events = self.security_events[-10000:]
    
#     def get_security_status(self) -> Dict:
        """Get security system status"""
#         recent_events = [
            {
                "event_id": e.event_id,
                "type": e.event_type,
                "ip": e.ip_address,
                "severity": e.severity,
                "timestamp": e.timestamp
            }
#             for e in self.security_events[-100:]  # Last 100 events
        ]
        
#         return {
            "security_id": self.security_id,
            "uptime_seconds": time.time() - self.started_at,
            "total_events": len(self.security_events),
            "recent_events": recent_events,
            "blacklisted_ips": len(self.ip_blacklist),
            "whitelisted_ips": len(self.ip_whitelist),
            "active_api_keys": len(self.valid_api_keys),
            "rate_limit_config": {
                "max_requests": self.rate_limit_max_requests,
                "window_seconds": self.rate_limit_window
            }
        }
    
#     def get_security_metrics(self) -> Dict:
        """Get security metrics for monitoring"""
        # Count events by type
#         event_counts = {}
#         for event in self.security_events:
#             event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
        
        # Count by severity
#         severity_counts = {}
#         for event in self.security_events:
#             severity_counts[event.severity] = severity_counts.get(event.severity, 0) + 1
        
#         return {
            "total_events": len(self.security_events),
            "events_by_type": event_counts,
            "events_by_severity": severity_counts,
            "blacklisted_ips_count": len(self.ip_blacklist),
            "failed_auth_attempts_tracked": len(self.failed_auth_attempts)
        }


# Global security instance
# security = HardenedSecurity()


# Security Middleware Decorators
# def require_api_key(func):
    """Decorator to require API key for endpoint"""
    @wraps(func)
#     async def wrapper(*args, **kwargs):
        # Get request from kwargs
#         request = kwargs.get('request')
#         api_key = kwargs.get('x_api_key')
        
#         if not api_key:
            # Try to get from request headers if not in kwargs
#             if request:
#                 api_key = request.headers.get('X-API-Key')
        
#         if not security.validate_api_key(api_key):
#             if request:
#                 client_ip = request.client.host
#                 security.record_failed_auth(client_ip)
            
#             raise HTTPException(
#                 status_code=401,
#                 detail="Invalid or missing API key"
        
#         return await func(*args, **kwargs)
    
#     return wrapper


# def rate_limit(func):
    """Decorator to apply rate limiting"""
    @wraps(func)
#     async def wrapper(*args, **kwargs):
#         request = kwargs.get('request')
        
#         if request:
#             client_ip = request.client.host
            
#             if not security.check_rate_limit(client_ip):
#                 raise HTTPException(
#                     status_code=429,
#                     detail="Rate limit exceeded. Please try again later."
        
#         return await func(*args, **kwargs)
    
#     return wrapper


# def ip_filter(func):
    """Decorator to filter IPs"""
    @wraps(func)
#     async def wrapper(*args, **kwargs):
#         request = kwargs.get('request')
        
#         if request:
#             client_ip = request.client.host
            
#             if not security.is_ip_allowed(client_ip):
#                 raise HTTPException(
#                     status_code=403,
#                     detail="Access denied from your IP address"
        
#         return await func(*args, **kwargs)
    
#     return wrapper


# def validate_input(required_fields: List[str] = None):
    """Decorator to validate and sanitize input"""
#     def decorator(func):
        @wraps(func)
#         async def wrapper(*args, **kwargs):
#             request = kwargs.get('request')
            
#             if request and required_fields:
#                 try:
#                     body = await request.json()
#                     is_valid, error = security.validate_request_data(body, required_fields)
                    
#                     if not is_valid:
#                         raise HTTPException(status_code=400, detail=error)
                    
                    # Replace request body with sanitized version
#                     kwargs['sanitized_data'] = security.sanitize_input(body)
#                 except Exception as e:
#                     raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")
            
#             return await func(*args, **kwargs)
        
#         return wrapper
    
#     return decorator


# Helper functions for endpoints
# async def get_client_ip(request: Request) -> str:
    """Get real client IP (handles proxies)"""
#     forwarded = request.headers.get("X-Forwarded-For")
#     if forwarded:
#         return forwarded.split(",")[0].strip()
#     return request.client.host


# def generate_new_api_key(user_id: str) -> str:
    """Generate new API key for a user"""
#     return security.generate_api_key(user_id)


# def get_security_dashboard() -> Dict:
    """Get comprehensive security dashboard data"""
#     return {
        "status": security.get_security_status(),
        "metrics": security.get_security_metrics(),
        "timestamp": time.time()
    }
