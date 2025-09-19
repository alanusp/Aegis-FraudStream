# Deploy to Cloud Run (Terraform)

```
cd deploy/cloudrun
terraform init
terraform apply -var="project_id=YOUR_GCP_PROJECT" -var="image=ghcr.io/OWNER/REPO:TAG"
```
