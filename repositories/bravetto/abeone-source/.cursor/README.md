# Cursor MCP Configuration

This directory contains the Model Context Protocol (MCP) configuration for the AIGuards Backend project.

## Files

### Configuration
- **`mcp-config.json`** - Main MCP server configuration
  - Configures AWS MCP server
  - Defines project AWS resources
  - Sets up capabilities and permissions

### Documentation
- **`aws-mcp-setup.md`** - Complete AWS MCP setup guide
  - Prerequisites and requirements
  - Service capabilities
  - Usage examples
  - Troubleshooting guide

### Setup Scripts
- **`setup-aws-credentials.sh`** - Linux/macOS credential setup script
- **`setup-aws-credentials.ps1`** - Windows PowerShell credential setup script

### Validation Scripts
- **`validate-aws-mcp.sh`** - Linux/macOS validation script
- **`validate-aws-mcp.ps1`** - Windows PowerShell validation script

## Quick Start

### 1. Setup AWS Credentials

**Windows:**
```powershell
.\.cursor\setup-aws-credentials.ps1
```

**Linux/macOS:**
```bash
./.cursor/setup-aws-credentials.sh
```

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

After setup and validation, restart Cursor to load the MCP configuration.

### 4. Test MCP Server

Try asking the AI:
- "List my ECS clusters"
- "Show ECR repositories"
- "Check Secrets Manager secrets"
- "View recent CloudWatch logs for the gateway service"

## What is MCP?

Model Context Protocol (MCP) is a standardized protocol that allows AI assistants to interact with external services and tools. The AWS MCP server provides the AI with the ability to:

- Query and manage AWS resources
- View CloudWatch logs
- Check service status
- List and describe infrastructure
- Monitor deployments

## AWS Services Accessible

The MCP configuration provides access to:

1. **ECS** - Container orchestration
2. **ECR** - Container registry
3. **Secrets Manager** - Secure configuration
4. **RDS** - PostgreSQL database
5. **ElastiCache** - Redis cache
6. **CloudWatch** - Logs and monitoring
7. **ALB** - Load balancing

## Prerequisites

- AWS CLI v2 installed and configured
- Node.js v16+ and NPX
- Valid AWS credentials with appropriate IAM permissions
- Internet connection (for NPX package downloads)

## Security

- Never commit AWS credentials to version control
- Use IAM roles when possible (especially in CI/CD)
- Enable MFA for production accounts
- Follow principle of least privilege for IAM permissions
- Rotate credentials regularly

## Troubleshooting

### MCP Server Not Loading
1. Check Cursor console for errors
2. Verify `mcp-config.json` is valid JSON
3. Ensure AWS credentials are configured
4. Restart Cursor

### Permission Errors
1. Verify IAM permissions match those in `aws-mcp-setup.md`
2. Test AWS CLI access: `aws sts get-caller-identity`
3. Check region matches your resources

### Connection Issues
1. Verify internet connection
2. Check AWS CLI version: `aws --version`
3. Test NPX access: `npx -y @modelcontextprotocol/server-aws --help`

## Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [Project DevOps Guide](../DEVOPS_GUIDE.md)
- [AWS Deployment Architecture](../codeguardians-gateway/codeguardians-gateway/docs/AWS_DEPLOYMENT_ARCHITECTURE.md)

## Support

For issues or questions:
1. Check `aws-mcp-setup.md` for detailed troubleshooting
2. Run validation script to identify issues
3. Review Cursor console logs
4. See project documentation in the parent directory


