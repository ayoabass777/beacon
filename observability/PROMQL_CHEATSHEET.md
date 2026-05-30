# PromQL for the Beacon dashboard (Phase 3)

Build the dashboard panels yourself — but here are the three queries to reach for.
Type them; don't paste. Knowing why each works is the skill IREN is testing.

**Throughput** (fetches per second):
    sum(rate(beacon_fetches_total[1m]))

**Error rate** (fraction of fetches failing) — this is your SLI:
    sum(rate(beacon_fetch_errors_total[5m])) / sum(rate(beacon_fetches_total[5m]))

**p95 latency** (95th-percentile fetch duration):
    histogram_quantile(0.95, sum(rate(beacon_fetch_duration_seconds_bucket[5m])) by (le))

SLO to write down: "99% of fetches succeed; p95 latency < 2s."
The error-rate query is the SLI that measures the first half; p95 measures the second.
