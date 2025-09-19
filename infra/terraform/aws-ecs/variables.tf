variable "region" { type = string }
variable "name" { type = string }
variable "image" { type = string }
variable "cpu" { type = number, default = 256 }
variable "memory" { type = number, default = 512 }
variable "execution_role_arn" { type = string }
variable "task_role_arn" { type = string }
variable "subnets" { type = list(string) }
variable "security_groups" { type = list(string) }
