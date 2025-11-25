# AWS MCP Server Setup Guide

## Overview
This document describes the AWS MCP (Model Context Protocol) server configuration for the AIGuards Backend project.

## Prerequisites

### 1. AWS CLI Installation
Ensure AWS CLI v2 is installed and configured:

```bash
# Check AWS CLI version
aws --version

# Configure AWS credentials if not already done
aws configure

# Verify AWS credentials
aws sts get-caller-identity
```

### 2. Node.js and NPX
The AWS MCP server requires Node.js (v16+) and npx:

```bash
# Check Node.js version
node --version

# Check npm version
npm --version
```

## MCP Configuration

### Configuration File Location
`.cursor/mcp-config.json`

### AWS Services Accessible via MCP

The MCP server provides access to the following AWS services used in this project:

#### 1. **ECS (Elastic Container Service)**
- **Cluster**: `codeguardians-gateway-cluster`
- **Services**: `codeguardians-gateway-service`
- **Tasks**: Running container instances
- **Capabilities**: Deploy, scale, monitor tasks

#### 2. **ECR (Elastic Container Registry)**
- **Repositories**:
  - `codeguardians-gateway`
  - `tokenguard`
  - `trustguard`
  - `contextguard`
  - `biasguard`
  - `healthguard`
- **Capabilities**: List images, push/pull, scan for vulnerabilities

#### 3. **Secrets Manager**
- **Secrets**: `codeguardians-gateway/production`
- **Capabilities**: Retrieve secrets, update secrets, rotate credentials

#### 4. **RDS (PostgreSQL)**
- **Connection**: Via DATABASE_URL secret
- **Capabilities**: Check status, describe instances

#### 5. **ElastiCache (Redis)**
- **Connection**: Via REDIS_URL secret
- **Capabilities**: Check cluster status, describe nodes

#### 6. **CloudWatch Logs**
- **Log Group**: `/ecs/codeguardians-gateway`
- **Capabilities**: View logs, stream logs, query logs

#### 7. **Application Load Balancer**
- **Capabilities**: Check health, describe target groups

## Usage Examples

### Via AI Assistant

Once configured, you can ask the AI assistant to:

1. **Check ECS Service Status**
   ```
   "Check the status of the codeguardians-gateway ECS service"
   ```

2. **View Recent Logs**
   ```
   "Show me the last 50 log entries from the gateway service"
   ```

3. **List ECR Images**
   ```
   "List all images in the codeguardians-gateway ECR repository"
   ```

4. **Check Secrets**
   ```
   "Verify that all required secrets exist in Secrets Manager"
   ```

5. **Monitor Task Health**
   ```
   "Check if all ECS tasks are healthy"
   ```

## Environment Variables

The MCP server uses the following environment variables:

### Required
- `AWS_REGION`: Default region (us-east-1)
- `AWS_PROFILE`: AWS credentials profile (default)

### Optional (if not using AWS CLI profile)
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_SESSION_TOKEN`: Session token (for temporary credentials)

## Security Considerations

### IAM Permissions Required

The AWS credentials used by the MCP server should have the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeClusters",
        "ecs:DescribeServices",
        "ecs:DescribeTasks",
        "ecs:ListTasks",
        "ecs:ListServices",
        "ecr:DescribeRepositories",
        "ecr:ListImages",
        "ecr:DescribeImages",
        "ecr:GetAuthorizationToken",
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecrets",
        "rds:DescribeDBInstances",
        "elasticache:DescribeCacheClusters",
        "elasticache:DescribeReplicationGroups",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "logs:FilterLogEvents",
        "elasticloadbalancing:DescribeLoadBalancers",
        "elasticloadbalancing:DescribeTargetGroups",
        "elasticloadbalancing:DescribeTargetHealth"
      ],
      "Resource": "*"
    }
  ]
}
```

### Best Practices
1. **Use IAM roles** when possible (especially for EC2/ECS instances)
2. **Enable MFA** for production access
3. **Use least privilege** - only grant necessary permissions
4. **Rotate credentials** regularly
5. **Never commit credentials** to version control

## Troubleshooting

### MCP Server Not Starting

**Symptom**: MCP server fails to initialize

**Solutions**:
1. Check AWS credentials:
   ```bash
   aws sts get-caller-identity
   ```

2. Verify Node.js installation:
   ```bash
   node --version
   npx --version
   ```

3. Test MCP package installation:
   ```bash
   npx -y @modelcontextprotocol/server-aws --version
   ```

### Permission Denied Errors

**Symptom**: "Access Denied" or "Unauthorized" errors

**Solutions**:
1. Verify IAM permissions match the policy above
2. Check AWS credential configuration:
   ```bash
   aws configure list
   ```

3. Test specific service access:
   ```bash
   aws ecs describe-clusters
   aws secretsmanager list-secrets
   ```

### Region Mismatch

**Symptom**: Resources not found

**Solutions**:
1. Verify AWS_REGION matches your resources:
   ```bash
   echo $AWS_REGION
   ```

2. Update MCP config if needed:
   ```json
   {
     "env": {
       "AWS_REGION": "your-actual-region"
     }
   }
   ```

## Testing the Setup

### 1. Test AWS CLI Access
```bash
# Test basic connectivity
aws sts get-caller-identity

# Test ECS access
aws ecs describe-clusters --cluster codeguardians-gateway-cluster

# Test ECR access
aws ecr describe-repositories

# Test Secrets Manager access
aws secretsmanager list-secrets
```

### 2. Test MCP Server
Once Cursor loads the MCP configuration, try asking:
```
"List all ECS clusters in my AWS account"
```

Expected: Should return cluster information including `codeguardians-gateway-cluster`

### 3. Test Full Integration
```
"Show me the status of all services in the codeguardians-gateway-cluster"
```

Expected: Should show service details, running tasks, and health status

## Additional Resources

- [AWS MCP Server Documentation](https://github.com/modelcontextprotocol/servers)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [AIGuards DevOps Guide](../DEVOPS_GUIDE.md)
- [AWS Deployment Architecture](../codeguardians-gateway/codeguardians-gateway/docs/AWS_DEPLOYMENT_ARCHITECTURE.md)

## Support

For issues with:
- **MCP Server**: Check Cursor logs and console
- **AWS Permissions**: Review IAM policies and credentials
- **AIGuards Infrastructure**: See DEVOPS_GUIDE.md and TROUBLESHOOTING.md


