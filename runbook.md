# Runbook — Beacon Fetcher

Fill the bracketed parts in during Phase 5, after you trigger and resolve the incident.

## Alert: BeaconHighErrorRate

**What it means:** the fetcher's error ratio has been above 5% for 5 minutes.

**Triage**
1. Open the Grafana "Beacon — Fetcher" dashboard. Confirm the error-rate panel is elevated.
2. Pivot to the Logs panel (LogQL) and read the recent error lines: `{app="fetcher"} |= "fetch failed"`.
3. Check dependencies: `kubectl get pods` — is Postgres or Redis down/CrashLooping?

**Likely causes & fixes**
- Postgres pod down → `kubectl get deploy postgres`; scale back up: `kubectl scale deploy/postgres --replicas=1`.
- Elevated `BEACON_FAILURE_RATE` config → check the ConfigMap / values.yaml.
- [add what you actually find]

**Verify recovery**
- Error-rate panel returns below 5%; alert resolves in Grafana.

---

## Postmortem — [date]

**Summary:** [one line: what broke, how long, impact]

**Timeline**
- [t0] Scaled Postgres to 0 replicas to simulate a dependency outage.
- [t1] BeaconHighErrorRate fired after ~5 min.
- [t2] Diagnosed via dashboard + logs.
- [t3] Restored Postgres; alert cleared.

**What worked:** [e.g. the alert fired as designed; logs pinpointed the cause fast]

**What I'd improve:** [e.g. add a readiness gate so the fetcher backs off when Postgres is unreachable]
