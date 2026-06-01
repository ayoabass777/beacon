# Runbook — Beacon Fetcher

## Alert: BeaconHighErrorRate

**What it means:** the fetcher's error ratio has been above 5% for 5 minutes.

**Triage**
1. Open the Grafana "Beacon Overview" dashboard. Confirm the error-rate panel is elevated.
2. Pivot to the Logs panel (LogQL) and read the recent error lines: `{app="fetcher"} |= "fetch failed"`.
3. Check dependencies: `kubectl get pods` — is Postgres or Redis down/CrashLooping?

**Likely causes & fixes**
- Postgres pod down → `kubectl get deploy postgres`; scale back up: `kubectl scale deploy/postgres --replicas=1`.
- Elevated `BEACON_FAILURE_RATE` config → check values.yaml or Helm release values: `helm get values beacon`. Fix with `helm upgrade beacon ./chart/beacon --set fetcher.failureRate=0.02`.
- Upstream dependency timeout → check fetcher logs for connection errors, verify service DNS resolution.

**Verify recovery**
- Error-rate panel returns below 5%; alert resolves in Grafana.
- Fetcher Logs panel stops showing `ERROR fetch failed` lines.

---

## Postmortem — 2026-06-01

**Summary:** Fetcher error rate spiked to ~35% for ~25 minutes after failure rate was set to 50% via Helm upgrade. Alert fired as designed. Resolved by rolling back the failure rate.

**Timeline**
- 04:28 — `helm upgrade` applied with `fetcher.failureRate=0.50` to simulate incident.
- 04:33 — Error Rate panel on Beacon Overview dashboard visibly spiked above 5%.
- 04:48 — `BeaconHighErrorRate` alert fired (5m `for` clause satisfied).
- 05:05 — Fix applied: `helm upgrade beacon ./chart/beacon --set fetcher.failureRate=0.02`.
- 05:10 — Error rate dropped below 5%; alert resolved to Normal.

**What worked:**
- The PrometheusRule alert fired correctly after the 5-minute threshold was sustained.
- The Grafana dashboard (error rate panel + logs panel) made diagnosis immediate — logs showed `fetch failed: simulated downstream failure` within seconds.
- The ServiceMonitor scrape pipeline (fetcher → Prometheus → Grafana) was reliable end-to-end.

**What I'd improve:**
- Add a readiness gate so the fetcher backs off when the failure rate is abnormally high, rather than continuing to hammer a failing dependency.
- Configure a notification channel (Slack/email) so the alert doesn't just sit in Grafana — it pages someone.
- Add a Grafana annotation on deploy so the dashboard shows exactly when the Helm upgrade happened.
