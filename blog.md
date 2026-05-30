# blog.md — Beacon write-up brief

Context and outline for the Dev.to post. Write the full post *after* Phase 5, while the incident is fresh. This file is the brief, not the final draft.

## Working title

"I gave my data pipeline a cockpit: adding observability to a Kubernetes deployment"

(Alternates: "From Docker Compose to a cockpit: observability on minikube" · "What I learned wiring Prometheus, Grafana, and Loki onto a k8s service")

## Audience & purpose

Hiring managers and engineers at infra/platform teams (IREN, Hootsuite, and similar Vancouver/remote shops). The post doubles as an outreach artifact: lead with value (share the post + repo for feedback) rather than a direct ask. Tone matches my existing Dev.to posts: technical, honest about tradeoffs, "what production would look like" framing — not a tutorial-mill walkthrough.

## The hook (mental model to open with)

My pipelines ran fine, but they were a car with a sealed hood and no dashboard — running, but no instruments to read and no way to swap a part without stopping. Beacon bolts on the dashboard (Prometheus + Grafana) and rebuilds the engine bay (Kubernetes). Open with this; it frames the whole post.

## Spine (what to cover, in order)

1. **The gap.** I had reliability *patterns* (DLQs, idempotency) but no reliability *visibility*. You can't be on-call for something you can't see.
2. **The setup.** One existing service (Sentinel fetcher) on minikube via Helm. Why reuse, not rebuild — the skill being shown is the platform layer.
3. **Metrics that matter.** The three I chose (throughput, p95 latency, error rate) and why those map to an SLO. Show one real PromQL query and explain it in plain English.
4. **Logs you can pivot to.** Loki + LogQL — the value isn't "logs exist," it's jumping from a latency spike on the graph to the exact error lines.
5. **The incident I caused on purpose.** This is the centerpiece. I scaled Postgres to zero, watched the alert fire, triaged from the dashboard, fixed it, and wrote the postmortem. Walk through it like a real on-call story.
6. **What production would differ.** Managed Prometheus/Grafana (or Datadog), real alert routing (PagerDuty), multi-replica, HA Postgres, proper RBAC. Name what I deliberately left out and why.
7. **What I'd tell past-me.** 2–3 honest lessons (e.g. "the alert is the easy part; the runbook is the job").

## Rules

- Honest only. Every claim reflects something actually built and run.
- One clear diagram (reuse the README mermaid).
- Show real snippets (a PromQL query, the alert rule, a kubectl command) — but small. Don't paste whole files.
- End with a soft CTA: repo link + "happy to hear how you'd harden this."

## Assets to pull in when writing

- Architecture diagram (README)
- A screenshot of the Grafana dashboard with the incident visible
- The alert rule YAML (`observability/alert-rule.yaml`)
- The postmortem paragraph from `runbook.md`

## Repurpose afterwards

- LinkedIn post: the incident story, condensed, with the "you can't be on-call for what you can't see" line as the hook.
- X/Twitter thread: one tweet per phase, screenshot of the dashboard as the lead image.
- (Use the content-manager skill to generate these from the finished post.)
