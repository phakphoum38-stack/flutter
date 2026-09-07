# Defensive API Integration V1.10

## Role

Flutter is an external client/tool. The server remains the source of truth for policy, authorization, entitlement, and execution decisions.

## Flow

```text
Flutter Client
    ↓ HTTPS
POST /v1/security/decision
    ↓
Server Decision Engine
    ↓
ALLOW / DENY
    ↓
Evidence / Audit
```

## Boundary

The client sends device/service/action inputs only. It must not submit a client-controlled authorization or decision value to force execution.

## Scope

This integration is for defensive security research and authorized workflows. It does not implement Activation Lock bypass, passcode bypass, MDM circumvention, credential theft, exploit delivery, unauthorized access, or security-control evasion.
