#!/usr/bin/env bash
# TUI wrapper using whiptail to call queztl-bootstrap

set -euo pipefail

if ! command -v whiptail >/dev/null 2>&1; then
  echo "whiptail not found. Install 'whiptail' or 'dialog' first."
  exit 1
fi

TITLE="Queztl-Core Git / Stack Installer"

choice=$(whiptail --title "$TITLE" --menu "Select deployment target:" 20 70 7 \
  "local" "Local machine (Docker Compose on this OS)" \
  "aws"   "AWS (ECR + ECS/EKS)" \
  "azure" "Azure (ACR + ACI/AKS)" \
  "gcp"   "GCP (GCR/Cloud Run/GKE)" \
  "k8s"   "Kubernetes Cluster (kubectl)" \
  "menu"  "Use advanced QueztlOS menu (full/backend/frontend/cluster/git)" \
  3>&1 1>&2 2>&3) || exit 0

case "$choice" in
  local)
    exec queztl-bootstrap --mode headless --provider local
    ;;
  aws)
    region=$(whiptail --inputbox "AWS Region:" 10 60 "us-east-1" 3>&1 1>&2 2>&3) || exit 1
    ecr=$(whiptail --inputbox "ECR repo name:" 10 60 "queztl-git" 3>&1 1>&2 2>&3) || exit 1
    exec queztl-bootstrap --mode headless --provider aws --aws-region "$region" --ecr-repo "$ecr"
    ;;
  azure)
    acr=$(whiptail --inputbox "Azure ACR name:" 10 60 "queztlregistry" 3>&1 1>&2 2>&3) || exit 1
    exec queztl-bootstrap --mode headless --provider azure --acr-name "$acr"
    ;;
  gcp)
    proj=$(whiptail --inputbox "GCP project ID:" 10 60 "queztl-core" 3>&1 1>&2 2>&3) || exit 1
    exec queztl-bootstrap --mode headless --provider gcp --gcp-project "$proj"
    ;;
  k8s)
    ns=$(whiptail --inputbox "K8s namespace:" 10 60 "queztl-git" 3>&1 1>&2 2>&3) || exit 1
    exec queztl-bootstrap --mode headless --provider k8s --k8s-namespace "$ns"
    ;;
  menu)
    exec queztl-bootstrap --mode headless
    ;;
esac
