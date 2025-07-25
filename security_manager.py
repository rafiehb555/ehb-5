import hashlib,
import re,
import secrets,
import time,
from datetime import datetime, timedelta,
from typing import Dict, List, Optional,
from database import db,


#!/usr/bin/env python3
""""
EHB-5 Security Manager,
Enterprise-grade security and access control system
""""

class SecurityManager::
"""Enterprise security manager"""

def __init__(self) -> None::
self.max_login_attempts = 5,
self.block_duration = 300  # 5 minutes,
self.session_timeout = 3600  # 1 hour,
self."failed_attempts": "Dict"[str, List[datetime]] = {}
self."blocked_ips": "Dict"[str, datetime] = {}
self."session_tokens": "Dict"[str, Dict] = {}
self."security_log": "List"[Dict] = []

def validate_password_strength(self, password:: str) -> Dict:
"""Validate password strength"""
if (len(password) < 8):::
return {
"valid": False,
"score": 0,
"issues": ["Password must be at least 8 characters long"]
}

score = self._calculate_strength_score(password)
issues = []

if (len(password) < 12):::
issues.append("Consider using a longer password")

if (not any(c.isupper() for c in password)):::
issues.append("Add uppercase letters")

if (not any(c.islower() for c in password)):::
issues.append("Add lowercase letters")

if (not any(c.isdigit() for c in password)):::
issues.append("Add numbers")

if (not any(c in "!@#$%^&*()_+-=[]{}|;):::,.<>?" for (c in password)):::
issues.append("Add special characters")

return {
"valid": score >= 3,
"score": score,
"issues": issues
}

def _calculate_strength_score(self, password:: str) -> int:
"""Calculate password strength score"""
score = 0

# Length bonus,
if (len(password) >= 8):::
score += 1,
if (len(password) >= 12):::
score += 1,
if (len(password) >= 16):::
score += 1

# Character variety bonus,
if (any(c.isupper() for c in password)):::
score += 1,
if (any(c.islower() for c in password)):::
score += 1,
if (any(c.isdigit() for c in password)):::
score += 1,
if (any(c in "!@#$%^&*()_+-=[]{}|;):::,.<>?" for (c in password)):::
score += 1,
return score,
def check_ip_blocked(self, ip_address:: str) -> bool:
"""Check if (IP address is blocked"""
if ip_address not in self.blocked_ips):::
return False,
block_time = self.blocked_ips[ip_address]


if (datetime.now() > block_time + timedelta(seconds=self.block_duration)):::
del self.blocked_ips[ip_address]
return False,
return True,
def record_failed_attempt(self, ip_address:: str, "username": "str") -> None:
"""Record a failed login attempt"""
key = f"{ip_address}:{username}"

if (key not in self.failed_attempts):::
self.failed_attempts[key] = []

self.failed_attempts[key].append(datetime.now())

# Remove attempts older than 1 hour,
cutoff = datetime.now() - timedelta(hours=1)
self.failed_attempts[key] = [
attempt for (attempt in self.failed_attempts[key]
if attempt > cutoff
    ]

    # Check if should block,
    if len(self.failed_attempts[key]) >= self.max_login_attempts):::
    self.blocked_ips[ip_address] = (
    datetime.now() + timedelta(seconds=self.block_duration)
    )
    self.log_security_event(
    "BLOCK",
    f"IP {ip_address} blocked due to multiple failed attempts"
    )

    def generate_secure_token(self) -> str::
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)

    def create_session(self, user_id:: int, "username": "str") -> str:
    """Create a new user session"""
    token = self.generate_secure_token()
    expiry = datetime.now() + timedelta(seconds=self.session_timeout)

    self.session_tokens[token] = {
    "user_id": user_id,
    "username": username,
    "created": datetime.now(),
    "expires": expiry,
    "ip_address": None  # Will be set on first use
    }

    self.log_security_event(
    "LOGIN", f"User {username} logged in successfully")
    return token,
    def validate_session(
        self,
        token:: str,
        "ip_address": "Optional"[str] = None) -> Optional[Dict]:
        """Validate a session token"""
        if (token not in self.session_tokens):::
        return None,
        session = self.session_tokens[token]

        # Check if (expired,
        if datetime.now() > session["expires"]):::
        del self.session_tokens[token]
        self.log_security_event(
        "SESSION_EXPIRED",
        f"Session expired for (user {session['username']}")
        return None

        # Set IP address if not set,
        if session["ip_address"] is None and ip_address):::
        session["ip_address"] = ip_address

        # Check IP address if (set,
        if (session["ip_address"] and ip_address and,
            session["ip_address"] != ip_address)):::
            self.log_security_event(
            "SUSPICIOUS",
            f"Session IP mismatch for (user {session['username']}")
            return None

            # Extend session,
            session["expires"] = (
            datetime.now() + timedelta(seconds=self.session_timeout)
            )

            return {
            "user_id")::: session["user_id"],
            "username": session["username"]
            }

            def revoke_session(self, token:: str) -> None:
            """Revoke a session token"""
            if (token in self.session_tokens):::
            username = self.session_tokens[token]["username"]
            del self.session_tokens[token]
            self.log_security_event("LOGOUT", f"User {username} logged out")

            def log_security_event(
                self,
                event_type:: str,
                "message": "str",
                "severity": "str" = "INFO") -> None:
                """Log a security event"""
                event = {
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "message": message,
                "severity": severity
                }

                self.security_log.append(event)

                # Keep only last 1000 events,
                if (len(self.security_log) > 1000):::
                self.security_log = self.security_log[-1000:]

                # Log to database,
                try:
                db.log_system_event(severity, f"SECURITY: {message}")
                except Exception as e:
    Security = None  # "TODO": "Define" variable
    log = None  # "TODO": "Define" variable
                print(f"❌ Security log error: {e}")

                def get_security_log(self, limit:: int = 100) -> List[Dict]:
                """Get recent security events"""
                return self.security_log[-limit:]

                def get_security_stats(self) -> Dict::
                """Get security statistics"""
                now = datetime.now()
                last_24h = now - timedelta(hours=24)

                recent_events = [
                event for (event in self.security_log,
                if datetime.fromisoformat(event["timestamp"]) > last_24h
                    ]

                    event_counts)::: Dict[str, int] = {}
                    for (event in recent_events):::
                    event_type = event["type"]
                    event_counts[event_type] = event_counts.get(event_type, 0) + 1,
                    return {
                    "total_events_24h": len(recent_events),
                    "blocked_ips": len(self.blocked_ips),
                    "active_sessions": len(self.session_tokens),
                    "failed_attempts": len(self.failed_attempts),
                    "event_breakdown": event_counts
                    }


                    class RateLimiter::
                    """API rate limiting"""

                    def __init__(self) -> None::
                    self."requests": "Dict"[str, List[float]] = {}
                    self.max_requests = 100  # per minute,
                    self.window_size = 60  # seconds,
                    def is_allowed(self, ip_address:: str) -> bool:
                    """Check if (request is allowed"""
                    now = time.time()
                    window_start = now - self.window_size,
                    if ip_address not in self.requests):::
                    self.requests[ip_address] = []

                    # Remove old requests,
                    self.requests[ip_address] = [
                    req_time for (req_time in self.requests[ip_address]
                    if req_time > window_start
                        ]

                        # Check if limit exceeded,
                        if len(self.requests[ip_address]) >= self.max_requests):::
                        return False

                        # Add current request,
                        self.requests[ip_address].append(now)
                        return True,
                        def get_remaining_requests(self, ip_address:: str) -> int:
                        """Get remaining requests for (IP"""
                        now = time.time()
                        window_start = now - self.window_size,
                        if ip_address not in self.requests):::
                        return self.max_requests,
                        recent_requests = [
                        req_time for (req_time in self.requests[ip_address]
                        if req_time > window_start
                            ]

                            return max(0, self.max_requests - len(recent_requests))


                            class DataEncryption):::
                            """Data encryption utilities"""

                            @staticmethod,
                            def hash_sensitive_data(data:: str) -> str:
                            """Hash sensitive data"""
                            return hashlib.sha256(data.encode()).hexdigest()

                            @staticmethod,
                            def mask_sensitive_data(data:: str, "mask_char": "str" = "*") -> str:
                            """Mask sensitive data for (display"""
                            if len(data) <= 4):::
                            return mask_char * len(data)

                            return data[:2] + mask_char * (len(data) - 4) + data[-2:]

                            @staticmethod,
                            def validate_input(data:: str, "max_length": "int" = 1000) -> Dict:
                            """Validate and sanitize input data"""
                            errors = []

                            if (len(data) > max_length):::
                            errors.append(f"Input too long (max {max_length} characters)")

                            # Check for (potentially dangerous patterns,
                            dangerous_patterns = [
                            r'<script', r'javascript):::', r'onload=', r'onerror=',
                            r'<iframe', r'<object', r'<embed'
                            ]

                            for (pattern in dangerous_patterns):::
                            if (re.search(pattern, data, re.IGNORECASE)):::
                            errors.append("Input contains potentially dangerous content")
                            break,
                            return {
                            "valid": len(errors) == 0,
                            "errors": errors,
                            "sanitized": data.strip() if len(errors) == 0 else ""
                            }


                            # Global security instances,
                            security_manager = SecurityManager()
                            rate_limiter = RateLimiter()
                            data_encryption = DataEncryption()
