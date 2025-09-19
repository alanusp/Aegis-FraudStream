terraform {
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}
provider "google" {
  project = var.project_id
  region  = var.region
}
variable "project_id" {}
variable "region" { default = "us-central1" }
variable "image"  { default = "ghcr.io/OWNER/REPO:latest" }

resource "google_cloud_run_v2_service" "aegis" {
  name     = "aegis-fraudstream"
  location = var.region
  template {
    containers {
      image = var.image
      ports { container_port = 8080 }
      env { name = "AEGIS_ENABLE_DOCS" value = "true" }
    }
  }
  ingress = "INGRESS_TRAFFIC_ALL"
}
