# AWS MCP Server - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Prerequisites ✅

Check if you have everything installed:

```powershell
# Windows PowerShell
aws --version          # Should show AWS CLI 2.x
node --version         # Should show Node.js 16+
npm --version          # Should show NPM 6+
```

**Missing something?**
- AWS CLI: https://awscli.amazonaws.com/AWSCLIV2.msi
- Node.js: https://nodejs.org/

### Step 2: Configure AWS Credentials 🔑

**Windows:**
```powershell
.\.cursor\setup-aws-credentials.ps1
```

**Linux/macOS:**
```bash
./.cursor/setup-aws-credentials.sh
```

You'll need:
- AWS Access Key ID (from AWS IAM console)
- AWS Secret Access Key (from AWS IAM console)
- AWS Region (e.g., `us-east-1`)

### Step 3: Validate Setup ✔️

**Windows:**
```powershell
.\.cursor\validate-aws-mcp.ps1
```

**Linux/macOS:**
```bash
./.cursor/validate-aws-mcp.sh
```

All tests should pass! ✨

### Step 4: Restart Cursor 🔄

Close and reopen Cursor to load the MCP configuration.

### Step 5: Test It! 🎉

Try asking the AI assistant:

**Basic Queries:**
- "List my AWS ECS clusters"
- "Show me all ECR repositories"
- "What secrets are in Secrets Manager?"

**Project-Specific:**
- "Check the status of the codeguardians-gateway ECS service"
- "Show recent logs from the gateway service"
- "List all images in the codeguardians-gateway ECR repository"

## 💡 What Can I Ask?

### ECS (Container Service)
- "List all ECS clusters"
- "Show services in the codeguardians-gateway-cluster"
- "What's the status of running ECS tasks?"
- "Describe the codeguardians-gateway-service"

### ECR (Container Registry)
- "List all ECR repositories"
- "Show images in the tokenguard repository"
- "What's the latest image tag for trustguard?"

### Secrets Manager
- "List all secrets"
- "Describe the codeguardians-gateway/production secret"
- "What keys are in the production secret?"

### CloudWatch Logs
- "Show recent logs from /ecs/codeguardians-gateway"
- "What errors are in the gateway logs?"
- "Display the last 100 log entries"

### General Infrastructure
- "Show me my AWS account information"
- "List all RDS databases"
- "What ElastiCache clusters exist?"

## 🔧 Troubleshooting

### "AWS credentials not configured"
```powershell
# Run the setup script again
.\.cursor\setup-aws-credentials.ps1

# Or manually configure
aws configure
```

### "Permission denied" errors
Check your IAM permissions match those in `aws-mcp-setup.md`

### "MCP server not found"
1. Check Node.js is installed: `node --version`
2. Verify NPX works: `npx --version`
3. Test MCP package: `npx -y @modelcontextprotocol/server-aws --help`

### MCP server not loading in Cursor
1. Check `.cursor/mcp-config.json` exists
2. Verify JSON is valid (no syntax errors)
3. Restart Cursor completely
4. Check Cursor console for error messages

## 📚 Next Steps

After setup, explore:
- Full documentation: `.cursor/aws-mcp-setup.md`
- Project DevOps guide: `DEVOPS_GUIDE.md`
- AWS deployment architecture: `codeguardians-gateway/codeguardians-gateway/docs/AWS_DEPLOYMENT_ARCHITECTURE.md`

## 🎯 Common Use Cases

### Checking Deployment Status
```
"Is the codeguardians-gateway service running?"
"How many tasks are running in the ECS cluster?"
"What's the health status of the gateway service?"
```

### Viewing Logs
```
"Show me the last 50 log entries from the gateway"
"Are there any errors in the CloudWatch logs?"
"Display logs from the past hour"
```

### Managing Images
```
"What's the latest image version in ECR?"
"List all image tags for the tokenguard repository"
"How many images are stored in ECR?"
```

### Checking Secrets
```
"What secrets are configured for production?"
"Verify the production secret exists"
"List all secrets in Secrets Manager"
```

## 🔐 Security Best Practices

- ✅ Use IAM roles when possible (especially in CI/CD)
- ✅ Enable MFA for production accounts
- ✅ Follow principle of least privilege
- ✅ Rotate credentials regularly
- ❌ Never commit credentials to Git
- ❌ Don't share credentials in plain text

## 📞 Getting Help

1. Run validation: `.\.cursor\validate-aws-mcp.ps1`
2. Check documentation: `.cursor/aws-mcp-setup.md`
3. Review project docs: `DEVOPS_GUIDE.md`
4. Check Cursor console for error messages

---

**Ready to go?** Restart Cursor and start asking questions about your AWS infrastructure! 🚀


