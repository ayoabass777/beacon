# CLAUDE.md — Beacon

Context for Claude Code (and any AI agent) working in this repo.

## What this project is

Beacon is a **learning + portfolio project**: deploy an existing service to local Kubernetes (minikube) and wrap it in full observability (Prometheus metrics, Grafana dashboards, Loki logs, alerting + runbook). It exists to build genuine hands-on Kubernetes and Grafana-stack experience and to produce a public artifact that demonstrates platform/DevOps/SRE competence.

It is **not** a product. There are no users. Optimize for clarity and learning, not features.

## Who I am (for tailoring help)

Self-directed engineer (CS BSc + MBA, Vancouver). Strong already in: Python, Terraform, AWS (S3/RDS), Docker, Kafka, dbt, Airflow, Postgres, Redis, reliability patterns (dead-letter queues, idempotency, transactional writes). **New to:** Kubernetes, the Grafana/Prometheus/Loki stack, Argo CD. Beacon is where I close that gap by doing.

I learn by building and by mental models/analogies. When explaining a k8s or observability concept, anchor it to something I already know (e.g. "a k8s Service is like a stable DNS name in front of a fleet of interchangeable workers" or relate it to Docker Compose, which I know well).

## How to help me

- **Teach, don't just do.** This is a learning project. When I'm stuck, explain the *why* and let me write the command — don't silently fix it for me. Pre-baked scaffolding exists so I can focus learning on the live parts (running the cluster, writing PromQL, triggering incidents).
- **Guard scope hard.** I have a known habit of scope creep. v1 = one service, one dashboard, one alert, one runbook. If I propose adding tracing/Tempo, a second app, or multi-cluster before Phase 5 is done, push back and tell me to ship first.
- **Phase order is the plan.** Don't jump ahead. Phases 1–5 are the weekend; 6–7 are stretch. See README for the phase list.
- **Honesty over polish.** Resume/blog claims must reflect what was actually built and run. No aspirational claims.

## The app

`app/fetcher.py` — a small worker reused from the Sentinel pipeline. It does a simple fetch-process loop against Postgres + Redis and exposes a Prometheus `/metrics` endpoint (FastAPI). The business logic is intentionally trivial; the metrics it emits are the point:
- `beacon_fetches_total` (counter)
- `beacon_fetch_duration_seconds` (histogram)
- `beacon_fetch_errors_total` (counter)

## Conventions

- Helm chart lives in `chart/beacon`; all tunables go in `values.yaml`, nothing hard-coded in templates.
- Secrets via k8s `Secret`, never in plaintext manifests or committed env files.
- Raw manifests in `k8s/` are the Phase-1 learning version; the Helm chart supersedes them from Phase 2 on. Keep them in sync or note which is canonical.
- Commit after each phase with a message naming the phase (e.g. `phase 3: prometheus scrape + grafana dashboard`).

## Current status

- [x] Repo scaffolded (manifests, chart, app, observability stubs, docs)
- [ ] Phase 1 — running on minikube
- [ ] Phase 2 — Helm
- [ ] Phase 3 — metrics + dashboard
- [ ] Phase 4 — logs
- [ ] Phase 5 — alert + runbook
- [ ] Phase 6 — Argo CD (stretch)
- [ ] Phase 7 — Terraform (stretch)

Update this checklist as phases complete — it's the single source of truth for where the project stands.

## Definition of done

Live demo: service on k8s → Grafana dashboard (metrics + logs) → triggerable alert → runbook. Then: update the IREN resume "Ramping on" line into a real Beacon bullet, and draft the blog post from `blog.md`.
