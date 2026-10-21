# Operations

> Purpose: how the running system is kept healthy. Required for the Critical tier. Update when infrastructure, alerts or procedures change. Owner: {{operations owner}}.

## Service objectives
| Objective | Target | Measured by |
|---|---|---|
| Availability | {{e.g. 99.9% per month}} | {{monitor}} |
| Recovery point (max data loss) | {{e.g. 15 minutes}} | {{backup configuration}} |
| Recovery time (max downtime after failure) | {{e.g. 1 hour}} | {{restore drill}} |

## Alerts
| Signal | Threshold | Who is notified | First action |
|---|---|---|---|
| {{Error rate}} | {{threshold}} | {{person or rota}} | {{runbook link}} |

## Runbooks
### Deploy
{{Steps, approvals, verification.}}

### Roll back
{{Steps to return to the last good release, including database considerations.}}

### Restore from backup
{{Steps, expected duration, last drill date and result.}}

### Incident
{{Declare, communicate, mitigate, review afterwards.}}

## Capacity and cost
- {{What is watched (database size, traffic, AI token spend), budget alerts, and scaling triggers}}
