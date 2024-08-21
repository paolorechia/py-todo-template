#!/bin/bash
# Source: https://grafana.com/docs/alloy/latest/set-up/install/kubernetes/

# We already installed loki, so we can skip updating helm chart here
kubectl create namespace alloy
helm install --namespace alloy alloy grafana/alloy