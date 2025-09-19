# Disaster Recovery Strategy

- **RTO**: 30 minutes target via DNS failover.
- **RPO**: 0 for stateless API; feature stores rely on Redis with cross-region replication if enabled.
- **Playbook**: Promote DR region by updating Route53 failover or Argo Rollouts with global load balancer.
