variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "project_number" {
  description = "Google Cloud Project Number"
  type        = string
}

variable "region" {
  description = "Default region for resources"
  type        = string
  default     = "us-central1"
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}