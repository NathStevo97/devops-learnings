---
tags:
  - Tooling
  - Grafana-Loki
---

# Using Centralized Logging

## 14.1 - Introduction

- Previously, logs were stored in files only.
- This was fine for static infrastructure running small application numbers.

- Now, infrastructure is dynamic and highly scalable. This made finding logs in files harder, a centralized system is needed to support distributed infrastructure.
- This is now a defacto standard in modern iinfrastructure.
  - Examples include:
    - Datadog
    - Splunk
    - ElasticSearch Logstash Kibana (ELK Stack) -> One of the most commonly used.
      - ELK has its issues, creating a high-resource consumption in-memory datastore.
        - Highly problematic when introducing scaling and sharding to clusters, amongst other operations / features.

## 14.2 - Using Loki

- Grafana introduced Loki as "like prometheus, but for logs".
- Prometheus is already a leading technology - Loki aimed to remove text-indexing, introducing labels to log lines in a similar vein to Prometheus metrics labels.
  - Loki actually uses the same metrics labelling library as Prometheus.

- Indexing is very compute-intensive, causing issues at scale. Using labels reduces the intensity; making it more efficient.
- Using the same set of labels from application logs and metrics helps with correlations.
- Logs are queried with PromQL - the same query language used by Prometheus for querying metrics. Specifically, Loki uses a subset of PromQL called LogQL.
  - Even if not using Prometheus, PromQL is being implemented across many tools, so using a subset makes sense and provides a good learning opportunity.

- The UI for exploring logs is based on Grafana - the defacto standard in observability.
- Grafana now has in-built support for Loki to query both logs and metrics in the same view from Loki and Prometheus respectively.

## 14.3 - Installing the Loki Stack

### Prerequisites

- Loki stack shall be run in Kubernetes
- Ingress is to be handled (for demo purposes) by the Nginx Ingress Controller.
  - Ingress address to be accessed shall be stored by the env variable `INGRESS_HOST`.
- Helm:
  - General use and to deploy the demo app.

### Supporting Links

- [Gist with Commands](https://gist.github.com/vfarcic/838a3a716cd9eb3c1a539a8d404d2077)
- [DevOps Toolkit - Monitoring Folder](https://github.com/vfarcic/devops-catalog-code/tree/master/monitoring)

### Steps

1. Create a monitoring namespace
1. Add Loki Repo and `helm repo update`
1. Install loki - the default values are suitable for testing
1. Install Grafana
1. Prometheus and Loki must be added as data sources and Ingress must be set up - use the provided YAMl as a base, and use `--set ingress.hosts="{grafana.$INGRESS_HOST.xip.io}"`
1. Install Prometheus via Helm
1. Check all is running as expected with `kubectl --namespace monitoring get pods`

### Notes

- When Loki is installed, there are "promtail" pods running.
  - Promtail pods run as daemonsets
  - They ship the contents of local logs by discovering targets in a similar manner to Proemtheus service discovery
  - They label the logs and ship them to a Loki instance and/or Grafana
- Additionally, a central Loki instance(s) runs, which handles the processing of the logs picked up by the Promtail pods.
- The logs can be stored by any suitable format e.g. S3.

- Prometheus discovers targets, scrapes and processes the metrics, which can then be viewed in Grafana.
  - Metrics are collected by the various exporters.
