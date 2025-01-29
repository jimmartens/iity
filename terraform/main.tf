terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "services" {
  for_each = toset([
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com"
  ])
  
  project = var.project_id
  service = each.key
  disable_on_destroy = false
}

# Cloud Build trigger
resource "google_cloudbuild_trigger" "main_trigger" {
  name = "main-branch-deploy"
  
  github {
    owner = var.github_owner
    name  = var.github_repo
    push {
      branch = "^main$"
    }
  }
  
  filename = "cloudbuild.yaml"
  
  depends_on = [google_project_service.services]
}

# IAM binding for Cloud Build to deploy to Cloud Run
resource "google_project_iam_binding" "cloudbuild_run" {
  project = var.project_id
  role    = "roles/run.admin"
  
  members = [
    "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
  ]
}

# IAM binding for Cloud Build to use service account
resource "google_project_iam_binding" "cloudbuild_sa" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  
  members = [
    "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
  ]
}