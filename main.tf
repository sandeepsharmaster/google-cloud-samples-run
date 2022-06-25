locals {
  common_tags = {
    Owner = "Sandeep Sharma"
    Description = "POC"
  }
}

resource "google_storage_bucket" "Input_Bucket" {
  name          = var.first_bucket
  storage_class = var.storage_class
  location      = "US-CENTRAL1"
  labels = {
    "env"    = "env"
    "author" = "sandy"
  }
  uniform_bucket_level_access = true
}

output "first_bucket" {
  value = google_storage_bucket.Input_Bucket.url
}

resource "google_storage_bucket" "Output_Bucket" {
  name          = var.second_bucket
  storage_class = "STANDARD"
  location      = "US-CENTRAL1"
  labels = {
    "env"    = "env"
    "author" = "sandy"
  }
  uniform_bucket_level_access = true
}

output "second_bucket" {
  value = google_storage_bucket.Output_Bucket.url
}


# Enables the Cloud Run API
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"

  disable_on_destroy = true
}

# Create the Cloud Run service
resource "google_cloud_run_service" "run_service" {
  name = "app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/poc-sandy-354205/cloudruntest:1.0.0"       
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  # Waits for the Cloud Run API to be enabled
  depends_on = [google_project_service.run_api]
}

# Allow unauthenticated users to invoke the service
resource "google_cloud_run_service_iam_member" "run_all_users" {
  service  = google_cloud_run_service.run_service.name
  location = google_cloud_run_service.run_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Display the service URL
output "service_url" {
  value = google_cloud_run_service.run_service.status[0].url
}