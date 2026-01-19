#!/usr/bin/env bash
# GUI wrapper using zenity to call queztl-bootstrap

set -euo pipefail

if ! command -v zenity >/dev/null 2>&1; then
  echo "zenity not found. Install zenity or use queztl-tui."
  exit 1
fi

choice=$(zenity --list \
  --title="Queztl-Core Installer" \
  --text="Select deployment target:" \
  --column="Target" --column="Description" \
  local "Local machine (Docker Compose on this OS)" \
  aws   "AWS (ECR + ECS/EKS)" \
  azure "Azure (ACR + ACI/AKS)" \
  gcp   "GCP (GCR/Cloud Run/GKE)" \
  k8s   "Kubernetes Cluster (kubectl)" \
  menu  "Advanced QueztlOS menu (full/backend/frontend/cluster/git)" \
  --width=520 --height=360) || exit 0

case "$choice" in
  local)
    exec queztl-bootstrap --mode gui --provider local
    ;;
  aws)
    region=$(zenity --entry --title="AWS Region" --text="Enter AWS region:" --entry-text="us-east-1") || exit 1
    ecr=$(zenity --entry --title="ECR Repo" --text="Enter ECR repo name:" --entry-text="queztl-git") || exit 1
    exec queztl-bootstrap --mode gui --provider aws --aws-region "$region" --ecr-repo "$ecr"
    ;;
  azure)
    acr=$(zenity --entry --title="Azure ACR Name" --text="Enter ACR name:" --entry-text="queztlregistry") || exit 1
    exec queztl-bootstrap --mode gui --provider azure --acr-name "$acr"
    ;;
  gcp)
    proj=$(zenity --entry --title="GCP Project" --text="Enter GCP project ID:" --entry-text="queztl-core") || exit 1
    exec queztl-bootstrap --mode gui --provider gcp --gcp-project "$proj"
    ;;
  k8s)
    ns=$(zenity --entry --title="K8s Namespace" --text="Enter namespace:" --entry-text="queztl-git") || exit 1
    exec queztl-bootstrap --mode gui --provider k8s --k8s-namespace "$ns"
    ;;
  menu)
    exec queztl-bootstrap --mode gui
    ;;
esac
