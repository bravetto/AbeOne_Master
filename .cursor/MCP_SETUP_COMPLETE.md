# AWS MCP Server Setup - Complete 

## Summary

The AWS Model Context Protocol (MCP) server has been successfully configured for the AIGuards Backend project. This enables AI-powered interaction with your AWS infrastructure directly from Cursor.

## What Was Configured

### 1. MCP Configuration File
**Location:** `.cursor/mcp-config.json`

Configured AWS MCP server with:
- AWS Region: `us-east-1`
- AWS Profile: `default`
- Project-specific AWS resources mapped
- Full capability definitions for all services

### 2. Documentation Created

| File | Purpose |
|------|---------|
| `aws-mcp-setup.md` | Complete setup guide, troubleshooting, security |
| `QUICK_START.md` | 5-minute quick start guide |
| `README.md` | Overview and directory structure |
| `MCP_SETUP_COMPLETE.md` | This summary document |

### 3. Setup Scripts

**Windows PowerShell:**
- `setup-aws-credentials.ps1` - Interactive AWS credential configuration
- `validate-aws-mcp.ps1` - Comprehensive validation testing

**Linux/macOS Bash:**
- `setup-aws-credentials.sh` - Interactive AWS credential configuration
- `validate-aws-mcp.sh` - Comprehensive validation testing

## AWS Services Accessible

The MCP server provides AI access to:

| Service | Resources | Capabilities |
|---------|-----------|-------------|
| **ECS** | `codeguardians-gateway-cluster` | List clusters, services, tasks; check status |
| **ECR** | 6 repositories (gateway + 5 guards) | List repositories, images, tags; check vulnerabilities |
| **Secrets Manager** | `codeguardians-gateway/production` | Retrieve secrets, list keys, describe configuration |
| **RDS** | PostgreSQL instances | Check status, describe instances |
| **ElastiCache** | Redis clusters | Check status, describe clusters |
| **CloudWatch** | `/ecs/codeguardians-gateway` | View logs, stream events, query patterns |
| **ALB** | Load balancers | Check health, describe target groups |

## Prerequisites Status

 **AWS CLI** - Installed (v2.31.18)
 **Node.js** - Installed (v22.19.0)
 **NPM** - Installed (v10.9.3)
  **AWS Credentials** - Not configured yet (needs setup)

## Next Steps

### 1. Configure AWS Credentials

**Windows:**
```powershell
.\.cursor\setup-aws-credentials.ps1
```

**Linux/macOS:**
```bash
./.cursor/setup-aws-credentials.sh
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- AWS Region (us-east-1 recommended)

### 2. Validate Setup

**Windows:**
```powershell
.\.cursor\validate-aws-mcp.ps1
```

**Linux/macOS:**
```bash
./.cursor/validate-aws-mcp.sh
```

### 3. Restart Cursor

Close and reopen Cursor to load the MCP configuration.

### 4. Test It!

Try asking the AI:
- "List my ECS clusters"
- "Show ECR repositories"
- "Check the gateway service status"

## Example Queries

Once configured, you can ask the AI assistant:

### Infrastructure Status
```
"What's the status of the codeguardians-gateway ECS service?"
"Are all ECS tasks running and healthy?"
"Show me the resource utilization of the gateway cluster"
```

### Deployment Verification
```
"List all images in the codeguardians-gateway ECR repository"
"What's the latest image tag for each guard service?"
"When was the last deployment to ECS?"
```

### Log Analysis
```
"Show recent errors from the gateway CloudWatch logs"
"Display the last 100 log entries"
"Are there any connection issues in the logs?"
```

### Configuration Management
```
"What secrets are configured in Secrets Manager?"
"Verify the production secret exists"
"List all environment variables in the ECS task definition"
```

## IAM Permissions Required

The AWS credentials need the following permissions:

**Core Services:**
- `ecs:Describe*`, `ecs:List*`
- `ecr:Describe*`, `ecr:List*`, `ecr:GetAuthorizationToken`
- `secretsmanager:GetSecretValue`, `secretsmanager:Describe*`, `secretsmanager:List*`
- `logs:Describe*`, `logs:GetLogEvents`, `logs:FilterLogEvents`

**Supporting Services:**
- `rds:DescribeDBInstances`
- `elasticache:Describe*`
- `elasticloadbalancing:Describe*`
- `sts:GetCallerIdentity`

See `aws-mcp-setup.md` for the complete IAM policy.

## Security Considerations

 **Configured:**
- MCP server uses AWS CLI credentials securely
- Environment variables for sensitive data
- Documentation includes security best practices

 **Important:**
- Never commit AWS credentials to Git
- Use IAM roles when possible (especially CI/CD)
- Enable MFA for production accounts
- Follow principle of least privilege
- Rotate credentials regularly

## File Structure

```
.cursor/
 mcp-config.json              # MCP server configuration
 aws-mcp-setup.md             # Complete setup guide
 QUICK_START.md               # 5-minute quick start
 README.md                    # Directory overview
 MCP_SETUP_COMPLETE.md        # This summary
 setup-aws-credentials.sh     # Linux/macOS setup script
 setup-aws-credentials.ps1    # Windows setup script
 validate-aws-mcp.sh          # Linux/macOS validation
 validate-aws-mcp.ps1         # Windows validation
```

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| AWS credentials not configured | Run `setup-aws-credentials.ps1` or `.sh` |
| Permission denied | Check IAM permissions in `aws-mcp-setup.md` |
| MCP server not loading | Verify `mcp-config.json`, restart Cursor |
| Node.js not found | Install from https://nodejs.org/ |
| Region mismatch | Update `AWS_REGION` in config or environment |

## Additional Resources

- **Quick Start:** `.cursor/QUICK_START.md`
- **Full Setup Guide:** `.cursor/aws-mcp-setup.md`
- **DevOps Guide:** `../DEVOPS_GUIDE.md`
- **AWS Architecture:** `../codeguardians-gateway/codeguardians-gateway/docs/AWS_DEPLOYMENT_ARCHITECTURE.md`

## Project Integration

This MCP setup integrates with the AIGuards Backend project's AWS infrastructure:

- **Gateway Service:** codeguardians-gateway on port 8000
- **Guard Services:** 6 specialized guard services (TokenGuard, TrustGuard, ContextGuard, BiasGuard, SecurityGuard, HealthGuard)
- **Database:** Neon PostgreSQL via Secrets Manager
- **Cache:** ElastiCache Redis via Secrets Manager
- **Deployment:** ECS Fargate with auto-scaling
- **Monitoring:** CloudWatch Logs and Metrics

## Success Criteria

Your setup is complete when:
-  AWS CLI is installed and configured
-  Node.js and NPM are installed
-  MCP configuration file exists and is valid
-  AWS credentials are configured
-  Validation script passes all tests
-  Cursor loads the MCP server without errors
-  AI can query AWS resources successfully

## Support

For help:
1. Run validation script to identify issues
2. Check `aws-mcp-setup.md` troubleshooting section
3. Review Cursor console for error messages
4. Verify IAM permissions match required policy
5. Test AWS CLI access: `aws sts get-caller-identity`

---

**Status:** MCP configuration complete, awaiting AWS credential setup

**Next Action:** Run `.\.cursor\setup-aws-credentials.ps1` (Windows) or `./.cursor/setup-aws-credentials.sh` (Linux/macOS)

**Estimated Setup Time:** 5 minutes

---

*Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")*


