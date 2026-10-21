# Security

> Purpose: what we protect, from whom, and how. Required for the Critical tier. Update with any change to sign-in, permissions, data handling or infrastructure. Owner: {{security owner}}.

## Data classification
| Class | Examples in this system | Rules |
|---|---|---|
| {{Restricted, e.g. health records}} | {{fields}} | {{encryption, access logging, retention}} |
| {{Personal}} | {{fields}} | {{rules}} |
| {{Internal}} | {{fields}} | {{rules}} |

## Threat model
| Asset or flow | Threat | Likelihood | Impact | Mitigation | Verified by |
|---|---|---|---|---|---|
| {{e.g. patient records API}} | {{e.g. user reads another clinic's records}} | {{L/M/H}} | {{L/M/H}} | {{e.g. tenant-scoped queries + row-level security}} | {{e.g. cross-tenant authorization tests in CI}} |

## Controls
- Identity and sign-in: {{provider, MFA policy, session lifetime}}
- Authorization: {{model and enforcement point}}
- Encryption: {{in transit and at rest; key management}}
- Audit logging: {{what is logged, retention, who can read it}}
- Supply chain: {{dependency policy, pinning, scanning}}
- Secrets: {{store, rotation, access}}

## Compliance mapping
| Obligation | Source (link, checked date) | How we meet it | Evidence |
|---|---|---|---|
| {{e.g. breach notification}} | {{source}} | {{process}} | {{where the evidence lives}} |

## Incident response
- Contacts: {{who is called}}
- First steps: {{contain, preserve evidence, notify}}
- Notification duties: {{who must be told, by when}}

## Professional review
{{Which parts a qualified human (security engineer, lawyer, compliance officer) must review, and status.}}
