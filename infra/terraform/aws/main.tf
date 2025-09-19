// Sample AWS infra (non-production). Requires variables and provider config.
terraform {
  required_version = ">= 1.6.0"
  required_providers { aws = { source = "hashicorp/aws" version = ">= 5.0" } }
}
provider "aws" { region = var.region }
variable "region" { type = string }
variable "name" { type = string }
resource "aws_db_subnet_group" "db" { name = "${var.name}-db" subnet_ids = [] }
# Add RDS and Elasticache per environment security constraints.
