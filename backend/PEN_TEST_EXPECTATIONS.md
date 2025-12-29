# 🛡️ PEN TESTING GUIDE & EXPECTATIONS

**Version**: 1.1.0  
**Date**: December 4, 2025  
**Target**: Queztl-Core Security Layer  
**Tester**: Security Team

---

## 📋 OVERVIEW

This document outlines expected behaviors, attack vectors, testing methodology, and success criteria for pen testing the new security layer in Queztl-Core v1.1.0.

### Scope of Testing

**In Scope**:
- ✅ Memory safety (leaks, use-after-free, double-free)
- ✅ Data sanitization (sensitive field leakage)
- ✅ API security (injection, authentication, authorization)
- ✅ DoS resilience (rate limiting, resource exhaustion)
- ✅ Audit logging (completeness, tampering)

**Out of Scope**:
- ❌ Infrastructure security (OS, network, Docker)
- ❌ Third-party dependencies (PostgreSQL, Redis)
- ❌ Physical security
- ❌ Social engineering

---

## 🎯 TESTING OBJECTIVES

1. **Validate** that security layer prevents memory leaks
2. **Verify** that sensitive data is never exposed in outputs
3. **Confirm** that injection attacks are blocked
4. **Test** DoS resilience under load
5. **Validate** audit logging captures all security events
6. **Verify** graceful degradation under attack

---

## 🔬 ATTACK VECTORS

### 1. Memory Safety Attacks

#### 1.1 Memory Exhaustion
**Objective**: Attempt to crash system by exhausting memory

**Attack Method**:
```python
import requests
import asyncio

# Rapid allocation without release
for i in range(10000):
    response = requests.post('http://localhost:8000/api/power/benchmark')
    # Don't wait for response to complete
```

**Expected Behavior**:
- ✅ System should detect allocation surge
- ✅ Memory manager should enforce limits
- ✅ Graceful rejection at 90% memory usage
- ✅ Audit log entry: "MEMORY_EXHAUSTION_DETECTED"
- ✅ HTTP 429 (Too Many Requests) or 503 (Service Unavailable)

**Success Criteria**:
- System remains responsive
- No crash or hang
- Automatic cleanup after load subsides
- Memory returns to baseline within 60 seconds

#### 1.2 Memory Leak Detection
**Objective**: Create scenario that leaks memory

**Attack Method**:
```python
# Allocate without releasing in loop
import numpy as np
for i in range(1000):
    huge_array = np.zeros((10000, 10000))  # 800MB
    # Intentionally don't release
```

**Expected Behavior**:
- ✅ Leak detected within 60 seconds
- ✅ Audit log entry: "MEMORY_LEAK_DETECTED" with stack trace
- ✅ Warning in security status endpoint
- ✅ Potential leak_mb reported accurately

**Success Criteria**:
- Leak detected when >100MB accumulated
- Stack trace identifies leak source
- Force cleanup endpoint works: `POST /api/security/cleanup`

#### 1.3 Use-After-Free Attempt
**Objective**: Try to access memory after it's been wiped

**Attack Method**:
```python
from security_layer import secure_allocate, secure_release

# Allocate and release
data = secure_allocate((1000, 1000))
secure_release(data)

# Attempt to access
try:
    print(data[0, 0])  # Should fail or return zero
except Exception as e:
    print(f"Prevented: {e}")
```

**Expected Behavior**:
- ✅ Memory wiped with 4-pass (0→1→random→0)
- ✅ Access returns zeros (memory cleared)
- ✅ No system information leakage

**Success Criteria**:
- No sensitive data accessible after release
- No crash or undefined behavior
- Memory zeroed out completely

### 2. Data Leakage Attacks

#### 2.1 Sensitive Field Exposure
**Objective**: Check if passwords/keys appear in responses

**Attack Method**:
```bash
# Create user with sensitive data
curl -X POST http://localhost:8000/api/users/create \
  -d '{"username": "test", "password": "secret123", "api_key": "sk-12345"}'

# Check various endpoints for leakage
curl http://localhost:8000/api/users/list
curl http://localhost:8000/api/security/audit
curl http://localhost:8000/api/security/status
```

**Expected Behavior**:
- ✅ Password appears as: `***REDACTED***`
- ✅ API key appears as: `***REDACTED***`
- ✅ Token appears as: `***REDACTED***`
- ✅ Applies to all outputs (JSON, logs, errors)

**Success Criteria**:
- Zero sensitive patterns in outputs
- Redaction patterns: `password`, `secret`, `key`, `token`, `api_key`, `private`, `credential`, `auth`, `session`

#### 2.2 Stack Trace Leakage
**Objective**: Trigger errors to see if stack traces expose internals

**Attack Method**:
```bash
# Send invalid inputs to trigger errors
curl -X POST http://localhost:8000/api/power/benchmark \
  -d '{"invalid": "data"}'

curl http://localhost:8000/api/nonexistent
curl http://localhost:8000/api/security/audit?count=99999999
```

**Expected Behavior**:
- ✅ Generic error messages only
- ✅ No internal paths exposed
- ✅ No database connection strings
- ✅ No implementation details

**Success Criteria**:
- Error responses contain: `{"error": "Invalid request"}` (generic)
- Stack traces logged to file, not sent to client
- Audit log captures error but sanitizes details

#### 2.3 Timing Attack on Sensitive Operations
**Objective**: Use timing to infer information

**Attack Method**:
```python
import time
import requests

# Measure response times
times = []
for i in range(100):
    start = time.time()
    response = requests.get('http://localhost:8000/api/security/memory')
    times.append(time.time() - start)

# Analyze variance
print(f"Mean: {sum(times)/len(times):.3f}s")
print(f"Variance: {max(times) - min(times):.3f}s")
```

**Expected Behavior**:
- ✅ Constant-time operations for sensitive data
- ✅ Variance <10ms for same operation
- ✅ No correlation between data and timing

**Success Criteria**:
- Timing variance minimal (<10ms)
- No exploitable timing channels

### 3. Injection Attacks

#### 3.1 SQL Injection
**Objective**: Attempt SQL injection through API

**Attack Method**:
```bash
# Try various SQL injection payloads
curl "http://localhost:8000/api/metrics/latest?limit=1' OR '1'='1"
curl "http://localhost:8000/api/users?id=1; DROP TABLE users;--"
curl "http://localhost:8000/api/search?q='; DELETE FROM metrics;--"
```

**Expected Behavior**:
- ✅ Parameterized queries prevent injection
- ✅ Malicious input sanitized or rejected
- ✅ Audit log entry: "INJECTION_ATTEMPT_DETECTED"
- ✅ HTTP 400 (Bad Request)

**Success Criteria**:
- Zero successful injections
- Database integrity maintained
- All attempts logged

#### 3.2 Command Injection
**Objective**: Attempt OS command execution

**Attack Method**:
```bash
# Try command injection in file operations
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.txt; rm -rf /"

# Try in parameters
curl "http://localhost:8000/api/process?command=ls; cat /etc/passwd"
```

**Expected Behavior**:
- ✅ No command execution
- ✅ Input validation blocks shell characters
- ✅ Audit log entry: "COMMAND_INJECTION_ATTEMPT"
- ✅ HTTP 400 (Bad Request)

**Success Criteria**:
- Zero command execution
- System files protected
- All attempts logged

#### 3.3 XSS (Cross-Site Scripting)
**Objective**: Inject JavaScript through API

**Attack Method**:
```bash
# Try XSS payloads
curl -X POST http://localhost:8000/api/comments/create \
  -d '{"text": "<script>alert(1)</script>"}'

curl -X POST http://localhost:8000/api/comments/create \
  -d '{"text": "<img src=x onerror=alert(1)>"}'
```

**Expected Behavior**:
- ✅ HTML/JavaScript escaped or stripped
- ✅ `<script>` becomes `[BLOCKED]`
- ✅ `onerror=` becomes `[BLOCKED]`
- ✅ Safe rendering in frontend

**Success Criteria**:
- Zero XSS execution
- Output properly escaped
- All attempts logged

### 4. DoS (Denial of Service) Attacks

#### 4.1 Rate Limiting Test
**Objective**: Verify rate limits work

**Attack Method**:
```python
import requests
import time

# Flood with requests
for i in range(10000):
    response = requests.get('http://localhost:8000/api/security/status')
    print(f"{i}: {response.status_code}")
```

**Expected Behavior**:
- ✅ Rate limit: 1000 requests/second per IP
- ✅ HTTP 429 after threshold
- ✅ Retry-After header present
- ✅ Audit log entry: "RATE_LIMIT_EXCEEDED"

**Success Criteria**:
- Rate limiting activates
- System remains responsive
- Legitimate requests still processed

#### 4.2 Resource Exhaustion
**Objective**: Exhaust CPU/memory

**Attack Method**:
```bash
# Request expensive operations
for i in {1..1000}; do
  curl -X POST http://localhost:8000/api/power/stress-test \
    -d '{"duration": 60, "intensity": "extreme"}' &
done
```

**Expected Behavior**:
- ✅ Queue limits enforced
- ✅ Graceful rejection at capacity
- ✅ HTTP 503 (Service Unavailable)
- ✅ Audit log entry: "RESOURCE_EXHAUSTION_DETECTED"

**Success Criteria**:
- System doesn't crash
- Memory stays <90%
- CPU stays <95%
- Recovery within 60 seconds

#### 4.3 Algorithmic Complexity Attack
**Objective**: Send worst-case inputs

**Attack Method**:
```bash
# Send extremely large arrays
curl -X POST http://localhost:8000/api/matrix/multiply \
  -d '{"size": 100000}'  # 100K x 100K matrix

# Send deeply nested JSON
curl -X POST http://localhost:8000/api/process \
  -d '{"a": {"b": {"c": {"d": ... (10000 levels) ... }}}}'
```

**Expected Behavior**:
- ✅ Input size limits enforced
- ✅ Nesting depth limits enforced
- ✅ HTTP 400 (Bad Request)
- ✅ Audit log entry: "COMPLEXITY_ATTACK_DETECTED"

**Success Criteria**:
- Limits: arrays <10M elements, nesting <100 levels
- No timeout or hang
- Fast rejection

### 5. Authentication/Authorization

#### 5.1 Bypass Attempts
**Objective**: Access protected endpoints without auth

**Attack Method**:
```bash
# Try without credentials
curl http://localhost:8000/api/admin/users
curl http://localhost:8000/api/security/cleanup -X POST

# Try with fake credentials
curl -H "Authorization: Bearer fake-token" \
  http://localhost:8000/api/admin/users
```

**Expected Behavior**:
- ✅ HTTP 401 (Unauthorized) for protected endpoints
- ✅ Audit log entry: "UNAUTHORIZED_ACCESS_ATTEMPT"
- ✅ No data leaked in error

**Success Criteria**:
- All protected endpoints secured
- Clear auth boundaries
- All attempts logged

---

## 📊 EXPECTED BASELINES

### Normal Operation

**Memory**:
- Baseline: 500MB
- Peak (under load): 2GB
- Leak threshold: 100MB growth
- Cleanup time: <60s

**Performance**:
- Throughput: 5.82B ops/sec
- Latency P50: 20ms
- Latency P95: 42ms
- Latency P99: 65ms

**API Response Times**:
- `/api/security/status`: <50ms
- `/api/security/memory`: <100ms
- `/api/security/audit`: <200ms
- `/api/power/benchmark`: 5-10s (normal)

**Security Events**:
- Normal: <10 events/minute (INFO level)
- Under attack: 100+ events/minute (WARNING/ERROR)

### Under Attack

**System Behavior**:
- Rate limiting activates at 1000 req/sec
- Memory rejection at 90% usage
- CPU throttling at 95% usage
- Graceful degradation, not crash

**Error Responses**:
- 400 Bad Request (invalid input)
- 401 Unauthorized (auth failure)
- 429 Too Many Requests (rate limit)
- 503 Service Unavailable (capacity)

**Security Alerts**:
- Memory leak: WARNING after 100MB
- Injection attempt: ERROR immediately
- Auth failure: WARNING after 5 attempts
- Resource exhaustion: CRITICAL immediately

---

## 🔍 TESTING METHODOLOGY

### Phase 1: Automated Scanning (4 hours)

```bash
# Install tools
pip install bandit safety pip-audit

# Security scanning
bandit -r backend/ -f json -o bandit-report.json
safety check --json > safety-report.json
pip-audit --format json > pip-audit-report.json

# Container scanning
docker scan queztl-backend:latest > docker-scan.txt

# OWASP ZAP automated scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:8000 -r zap-report.html
```

### Phase 2: Manual Testing (8 hours)

**Hour 1-2: Memory Safety**
- Run memory exhaustion tests
- Create leak scenarios
- Test use-after-free
- Verify cleanup mechanisms

**Hour 3-4: Data Leakage**
- Test sensitive field redaction
- Trigger errors, check stack traces
- Timing analysis
- Log file inspection

**Hour 5-6: Injection Attacks**
- SQL injection attempts
- Command injection attempts
- XSS payload testing
- Path traversal attempts

**Hour 7-8: DoS & Load Testing**
- Rate limiting validation
- Resource exhaustion tests
- Algorithmic complexity attacks
- Recovery time measurement

### Phase 3: Stress Testing (4 hours)

```bash
# Load testing with locust
locust -f locustfile.py --host=http://localhost:8000 \
  --users 10000 --spawn-rate 100 --run-time 1h

# Monitor during test
watch -n 1 'curl -s http://localhost:8000/api/security/memory | jq'
```

### Phase 4: Reporting (4 hours)

**Report Structure**:
1. Executive Summary
2. Vulnerabilities Found (Critical, High, Medium, Low)
3. Attack Vector Results
4. Performance Under Attack
5. Recommendations
6. Remediation Plan

---

## ✅ SUCCESS CRITERIA

### Critical (Must Pass)

- [ ] **Zero data leakage**: No sensitive info in outputs
- [ ] **Zero memory leaks**: <100MB growth in 24hr test
- [ ] **Zero injection success**: All injection attempts blocked
- [ ] **No crashes**: System remains stable under attack
- [ ] **Complete audit trail**: All security events logged

### High Priority (Should Pass)

- [ ] **Rate limiting effective**: DoS attacks mitigated
- [ ] **Graceful degradation**: No hard failures under load
- [ ] **Fast recovery**: <60s to return to baseline
- [ ] **Generic errors**: No internal details exposed
- [ ] **Constant-time ops**: No timing attacks possible

### Medium Priority (Nice to Have)

- [ ] **Performance overhead <5%**: Minimal security cost
- [ ] **Auto-recovery**: Self-healing after attacks
- [ ] **Intelligent throttling**: Adaptive rate limiting
- [ ] **Anomaly detection**: Unusual patterns detected

---

## 🚨 CRITICAL FINDINGS PROTOCOL

If a **CRITICAL** vulnerability is found:

1. **STOP testing immediately**
2. **Document the vulnerability** (steps to reproduce)
3. **Notify dev team** (security@queztl-core.com)
4. **Do not disclose** publicly
5. **Wait for patch** before continuing
6. **Re-test after fix**

Critical vulnerabilities:
- Remote code execution (RCE)
- SQL injection success
- Authentication bypass
- Data exfiltration
- System crash

---

## 📋 TESTING CHECKLIST

### Pre-Testing
- [ ] Test environment set up (isolated)
- [ ] Baseline measurements taken
- [ ] Monitoring configured
- [ ] Rollback plan ready
- [ ] Team on standby

### During Testing
- [ ] All attack vectors tested
- [ ] Results documented in real-time
- [ ] Screenshots/logs captured
- [ ] Performance metrics recorded
- [ ] Team communication active

### Post-Testing
- [ ] Full report generated
- [ ] Vulnerabilities prioritized
- [ ] Remediation plan created
- [ ] Follow-up scheduled
- [ ] Lessons learned documented

---

## 📊 REPORTING TEMPLATE

```markdown
# Pen Testing Report: Queztl-Core v1.1.0

## Executive Summary
- Test Date: [DATE]
- Tester: [NAME]
- Duration: [HOURS]
- Scope: Security Layer + Performance Optimizer

## Findings Summary
- Critical: [COUNT]
- High: [COUNT]
- Medium: [COUNT]
- Low: [COUNT]
- Informational: [COUNT]

## Critical Findings
1. [FINDING NAME]
   - Severity: Critical
   - Description: [...]
   - Steps to Reproduce: [...]
   - Impact: [...]
   - Recommendation: [...]

## Test Results by Category
- Memory Safety: PASS/FAIL
- Data Leakage: PASS/FAIL
- Injection Attacks: PASS/FAIL
- DoS Resilience: PASS/FAIL
- Authentication: PASS/FAIL

## Performance Under Attack
- Throughput: [BASELINE] → [UNDER ATTACK]
- Latency P95: [BASELINE] → [UNDER ATTACK]
- Memory: [BASELINE] → [PEAK]
- Recovery Time: [SECONDS]

## Recommendations
1. [HIGH PRIORITY]
2. [MEDIUM PRIORITY]
3. [LOW PRIORITY]

## Remediation Plan
- Critical fixes: [TIMELINE]
- High priority: [TIMELINE]
- Medium priority: [TIMELINE]

## Sign-Off
- Tester: [SIGNATURE]
- Date: [DATE]
- Status: APPROVED / NEEDS FIXES
```

---

## 🎯 CONCLUSION

This guide provides a comprehensive framework for pen testing the Queztl-Core security layer. Follow the methodology, document findings thoroughly, and communicate critical issues immediately.

**Remember**: The goal is to find vulnerabilities **before** attackers do. Be thorough, be creative, and be responsible.

Good hunting! 🕵️‍♂️🛡️

---

**Document Version**: 1.0  
**Last Updated**: December 4, 2025  
**Owner**: Security Team  
**Status**: Ready for Testing
