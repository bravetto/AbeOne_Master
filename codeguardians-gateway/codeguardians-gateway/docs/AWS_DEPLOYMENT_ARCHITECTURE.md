# AWS Deployment Architecture for CodeGuardians Gateway

## Overview

This document provides comprehensive guidance for deploying the CodeGuardians Gateway backend to AWS using ECS, ECR, and AWS Secrets Manager. The architecture ensures secure secrets management, internal guard service communication, and a unified API endpoint.

## Architecture Diagram

```

                        AWS Cloud                                
                                                                 
        
     Application                  Infrastructure              
     Load Balancer                                            
           
                                  ECS Cluster               
                                                             
                               
             Gateway Service             
     ECS Service            (Port 8000)                   
                                                          
                   
       Gateway               Guard Services           
      Container             (Internal Only)           
                                                       
                        
      TokenGuard             SecurityGuard         
      TrustGuard             ContextGuard          
      BiasGuard              HealthGuard           
                        
                   
             
                             
                                                               
                             
                                   RDS PostgreSQL            
                             
                                                               
                             
                                ElastiCache Redis            
                             
                          
                                                                 
   
                AWS Secrets Manager                            
                                                                
        
      codeguardians-gateway/production                      
       SECRET_KEY                                          
       DATABASE_URL                                        
       REDIS_URL                                           
       ...                                                 
        
   

```

## Key Components

### 1. Docker Compose Architecture
- **Single Host**: All services run on one server/VM
- **Internal Network**: Guards communicate via Docker network
- **External Access**: Only port 8000 (Gateway API) exposed
- **Health Checks**: Built-in Docker health checks

### 3. Guard Services (Internal Only)
- **TokenGuard**: Port 8001 (token optimization)
- **TrustGuard**: Port 8002 (trust validation)
- **ContextGuard**: Port 8003 (context analysis)
- **BiasGuard**: Port 8004 (bias detection)
- **SecurityGuard**: Port 8005 (security scanning)
- **HealthGuard**: Port 8005 (health monitoring)

### 4. Data Layer
- **RDS PostgreSQL**: Primary database
- **ElastiCache Redis**: Caching and session storage
- **Backup**: Automated backups with point-in-time recovery

### 5. Secrets Management
- **AWS Secrets Manager**: Centralized secrets storage
- **IAM Roles**: Task-level permissions
- **Encryption**: KMS encryption at rest and in transit

## Network Architecture

### VPC Configuration
```

                        VPC (10.0.0.0/16)                    
                                                             
                  
    Public Subnet                  Private Subnet       
    (10.0.1.0/24)                  (10.0.2.0/24)        
                                                        
                      
         ALB                        ECS Tasks       
                                                    
      Internet                       
      Gateway                         Gateway     
                        + Guards     
                      
                                       
                                     
                                                             
   
                Database Subnet                             
                (10.0.3.0/24)                              
                                                            
          
       RDS Instance          ElastiCache Cluster        
       PostgreSQL                 Redis                 
          
   

```

### Security Groups

#### Application Load Balancer
- **Inbound**: HTTPS (443) from 0.0.0.0/0
- **Outbound**: HTTP (8000) to ECS tasks

#### ECS Tasks
- **Inbound**: HTTP (8000) from ALB
- **Inbound**: Internal communication (8001-8005) from same security group
- **Outbound**: HTTPS (443) to AWS Secrets Manager
- **Outbound**: PostgreSQL (5432) to RDS
- **Outbound**: Redis (6379) to ElastiCache

#### RDS Database
- **Inbound**: PostgreSQL (5432) from ECS tasks only

#### ElastiCache Redis
- **Inbound**: Redis (6379) from ECS tasks only

## AWS Secrets Manager Structure

### Secret Hierarchy
```
codeguardians-gateway/
 production/                    # Main application secrets
    SECRET_KEY
    DATABASE_URL
    REDIS_URL
    ALLOWED_ORIGINS
    ALLOWED_HOSTS
 production/database/           # Database credentials
    username
    password
    host
    port
    database
 production/redis/              # Redis credentials
    host
    port
    password
    database
 production/optional/           # Optional service secrets
     CLERK_SECRET_KEY
     STRIPE_SECRET_KEY
     STRIPE_WEBHOOK_SECRET
```

### IAM Policy for ECS Task Role
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:codeguardians-gateway/production*"
      ]
    }
  ]
}
```

## ECS Task Definition

### Container Configuration
```json
{
  "family": "codeguardians-gateway",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "4096",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/codeguardians-gateway-task-role",
  "containerDefinitions": [
    {
      "name": "gateway",
      "image": "ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:codeguardians-gateway/production:SECRET_KEY::"
        },
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:codeguardians-gateway/production:DATABASE_URL::"
        },
        {
          "name": "REDIS_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:codeguardians-gateway/production:REDIS_URL::"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        },
        {
          "name": "AWS_SECRETS_ENABLED",
          "value": "true"
        },
        {
          "name": "AWS_SECRETS_NAME",
          "value": "codeguardians-gateway/production"
        },
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/codeguardians-gateway",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health/live || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

## Guard Services Internal Communication

### Service Discovery
- **Method**: Docker internal networking
- **URLs**: `http://localhost:PORT` within container
- **Health Checks**: Each guard exposes `/health` endpoint
- **Circuit Breakers**: Automatic failover for unhealthy services

### Communication Flow
```
Client Request
     
     

   Load Balancer 
   (Port 443)    

     
     

   Gateway       
   (Port 8000)   

     
     

              Guard Orchestrator                        
                                                         
             
   TokenGuard    TrustGuard  ContextGuard         
   (Port 8001)   (Port 8002)  (Port 8003)         
             
                                                         
             
    BiasGuard   SecurityGuard  HealthGuard          
   (Port 8004)   (Port 8005)   (Port 8005)          
             

```

## Monitoring and Logging

### CloudWatch Integration
- **Log Groups**: `/ecs/codeguardians-gateway`
- **Metrics**: CPU, Memory, Request count, Error rate
- **Alarms**: High error rate, low health check success
- **Dashboards**: Application performance monitoring

### Health Checks
- **Liveness**: `/health/live` - Application is running
- **Readiness**: `/health/ready` - Application can serve requests
- **Guard Health**: Individual guard service health monitoring

## Security Best Practices

### 1. Network Security
- **Private Subnets**: ECS tasks in private subnets only
- **Security Groups**: Restrictive inbound/outbound rules
- **NACLs**: Additional network-level security
- **VPC Endpoints**: Private access to AWS services

### 2. Secrets Management
- **No Hardcoded Secrets**: All secrets in AWS Secrets Manager
- **IAM Roles**: Task-level permissions (no access keys)
- **Encryption**: KMS encryption for all secrets
- **Rotation**: Automated secret rotation policies

### 3. Container Security
- **Base Images**: Minimal, security-scanned base images
- **Non-root User**: Containers run as non-root
- **Resource Limits**: CPU and memory limits
- **Read-only Filesystem**: Where possible

### 4. Data Protection
- **Encryption at Rest**: RDS and ElastiCache encryption
- **Encryption in Transit**: TLS for all communications
- **Backup Encryption**: Encrypted database backups
- **Access Logging**: CloudTrail for audit trails

## Deployment Workflow

### 1. Pre-deployment
```bash
# Build and push Docker image
docker build -t codeguardians-gateway .
docker tag codeguardians-gateway:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest

# Update secrets in AWS Secrets Manager
./scripts/setup_aws_secrets.sh us-east-1 codeguardians-gateway/production
```

### 2. Infrastructure Deployment
```bash
# Deploy infrastructure with Terraform/CloudFormation
terraform apply -var="environment=production"
```

### 3. Application Deployment
```bash
# Update ECS service
aws ecs update-service --cluster codeguardians-gateway --service gateway-service --force-new-deployment
```

### 4. Post-deployment Validation
```bash
# Health check
curl -f https://your-alb-dns-name/health/live

# API test
curl -X POST https://your-alb-dns-name/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"text": "test", "service_type": "tokenguard"}'
```

## Terraform Module Structure

### Directory Layout
```
terraform/
 main.tf                 # Main configuration
 variables.tf            # Input variables
 outputs.tf              # Output values
 modules/
    ecs/               # ECS cluster and service
    networking/        # VPC, subnets, security groups
    database/          # RDS PostgreSQL
    cache/            # ElastiCache Redis
    secrets/           # AWS Secrets Manager
    monitoring/        # CloudWatch, alarms
 environments/
     production/        # Production environment
     staging/          # Staging environment
```

### Key Terraform Resources
- **ECS Cluster**: `aws_ecs_cluster`
- **ECS Service**: `aws_ecs_service`
- **Task Definition**: `aws_ecs_task_definition`
- **Application Load Balancer**: `aws_lb`
- **RDS Instance**: `aws_db_instance`
- **ElastiCache**: `aws_elasticache_replication_group`
- **Secrets Manager**: `aws_secretsmanager_secret`

## Troubleshooting

### Common Issues

#### 1. Secrets Not Loading
- **Check**: IAM permissions for ECS task role
- **Check**: Secret ARN in task definition
- **Check**: AWS region configuration

#### 2. Guard Services Not Starting
- **Check**: Internal network connectivity
- **Check**: Health check endpoints
- **Check**: Resource limits (CPU/Memory)

#### 3. Database Connection Issues
- **Check**: Security group rules
- **Check**: Database credentials in secrets
- **Check**: RDS instance status

#### 4. Load Balancer Health Check Failures
- **Check**: Target group health
- **Check**: Security group rules
- **Check**: Application logs in CloudWatch

### Debugging Commands
```bash
# Check ECS service status
aws ecs describe-services --cluster codeguardians-gateway --services gateway-service

# View application logs
aws logs tail /ecs/codeguardians-gateway --follow

# Test secrets access
aws secretsmanager get-secret-value --secret-id codeguardians-gateway/production

# Check security groups
aws ec2 describe-security-groups --group-ids sg-xxxxxxxxx
```

## Cost Optimization

### 1. Resource Sizing
- **ECS Tasks**: Right-size CPU and memory
- **RDS**: Use appropriate instance class
- **ElastiCache**: Optimize node type and count

### 2. Auto-scaling
- **ECS Service**: Scale based on CPU/memory
- **RDS**: Read replicas for read-heavy workloads
- **ElastiCache**: Cluster mode for high availability

### 3. Monitoring Costs
- **CloudWatch**: Set up billing alarms
- **Cost Explorer**: Regular cost analysis
- **Reserved Instances**: For predictable workloads

## Disaster Recovery

### 1. Backup Strategy
- **RDS**: Automated backups with point-in-time recovery
- **ElastiCache**: Snapshot backups
- **Secrets**: Cross-region replication

### 2. Multi-Region Deployment
- **Active-Passive**: Primary region with standby
- **Cross-Region Replication**: Database and cache replication
- **DNS Failover**: Route53 health checks

### 3. Recovery Procedures
- **RTO**: 4 hours (Recovery Time Objective)
- **RPO**: 1 hour (Recovery Point Objective)
- **Automated Failover**: For critical services

## Compliance and Governance

### 1. Security Compliance
- **SOC 2**: Security controls implementation
- **PCI DSS**: If handling payment data
- **GDPR**: Data protection and privacy

### 2. Audit and Monitoring
- **CloudTrail**: API call logging
- **Config**: Resource configuration tracking
- **GuardDuty**: Threat detection

### 3. Access Control
- **IAM**: Role-based access control
- **MFA**: Multi-factor authentication
- **Least Privilege**: Minimal required permissions

---

## Quick Reference

### Essential Commands
```bash
# Deploy application
./scripts/setup_aws_secrets.sh
terraform apply
aws ecs update-service --cluster codeguardians-gateway --service gateway-service --force-new-deployment

# Monitor application
aws logs tail /ecs/codeguardians-gateway --follow
curl -f https://your-alb-dns-name/health/live

# Update secrets
aws secretsmanager update-secret --secret-id codeguardians-gateway/production --secret-string '{"SECRET_KEY": "new-key"}'
```

### Key URLs
- **API Endpoint**: `https://your-alb-dns-name/api/v1/guards/process`
- **Health Check**: `https://your-alb-dns-name/health/live`
- **API Documentation**: `https://your-alb-dns-name/docs`

### Important ARNs
- **ECS Cluster**: `arn:aws:ecs:us-east-1:ACCOUNT_ID:cluster/codeguardians-gateway`
- **Task Role**: `arn:aws:iam::ACCOUNT_ID:role/codeguardians-gateway-task-role`
- **Secrets**: `arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:codeguardians-gateway/production`
