# Phase 7 (stretch) — install the monitoring stack as code instead of by hand.
# Now the observability PLATFORM itself is version-controlled.
terraform {
  required_providers {
    helm = { source = "hashicorp/helm", version = "~> 2.13" }
  }
}

provider "helm" {
  kubernetes { config_path = "~/.kube/config" }  # minikube context
}

resource "helm_release" "kube_prometheus_stack" {
  name             = "kube-prometheus-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true
}

resource "helm_release" "loki_stack" {
  name             = "loki"
  repository       = "https://grafana.github.io/helm-charts"
  chart            = "loki-stack"
  namespace        = "monitoring"
  create_namespace = true
  set {
    name  = "promtail.enabled"
    value = "true"
  }
}
