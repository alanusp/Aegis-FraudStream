terraform {
  backend "s3" {}
  required_providers { aws = { source = "hashicorp/aws", version = "~>5.0" } }
}
provider "aws" { region = var.primary_region }
provider "aws" { alias = "dr"; region = var.dr_region }

resource "aws_route53_health_check" "primary" {
  fqdn = var.primary_dns
  port = 443
  type = "HTTPS"
  resource_path = "/health"
}
resource "aws_route53_record" "failover" {
  zone_id = var.zone_id
  name    = var.app_dns
  type    = "A"
  set_identifier = "primary"
  failover_routing_policy { type = "PRIMARY" }
  alias {
    name                   = var.primary_alb_dns
    zone_id                = var.primary_alb_zone_id
    evaluate_target_health = true
  }
}
