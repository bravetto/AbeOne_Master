# AWS MCP Server Architecture

## Overview

This document describes the architecture of the AWS Model Context Protocol (MCP) server integration with the AIGuards Backend project.

## Architecture Diagram

```

                          CURSOR IDE                                  
                                                                      
   
                      AI Assistant (Claude)                         
                                                                    
    User Query: "Check ECS service status"                         
   
                                                                     
                             MCP Protocol                            
                                                                     
   
                AWS MCP Server (Node.js/NPX)                       
                                                                    
    Configuration: .cursor/mcp-config.json                         
    - AWS Region: us-east-1                                        
    - AWS Profile: default                                         
    - Project Resources: AIGuards Infrastructure                   
   

                             
                              AWS SDK / CLI
                             

                        AWS CLOUD                                     
                                                                      
        
      ECS / ECR        Secrets Manager       CloudWatch       
                                                              
   • Clusters          • Secrets           • Logs             
   • Services          • Keys              • Metrics          
   • Tasks             • Configuration     • Events           
   • Images                                                   
        
                                                                      
        
     RDS / Redis             ALB                 IAM          
                                                              
   • PostgreSQL        • Load Balancer     • Permissions      
   • ElastiCache       • Target Groups     • Roles            
   • Connections       • Health Checks     • Policies         
                                                              
        

```

## Component Details

### 1. Cursor IDE
- **Purpose**: Development environment hosting the AI assistant
- **Role**: User interface for interacting with AWS via AI
- **Integration**: Loads MCP configuration on startup

### 2. AI Assistant (Claude Sonnet 4.5)
- **Purpose**: Natural language interface to AWS infrastructure
- **Capabilities**: 
  - Interpret user queries about AWS resources
  - Make MCP protocol calls to AWS server
  - Present results in natural language
  - Provide recommendations and insights

### 3. AWS MCP Server
- **Runtime**: Node.js via NPX
- **Package**: `@modelcontextprotocol/server-aws`
- **Configuration**: `.cursor/mcp-config.json`
- **Authentication**: AWS CLI credentials
- **Capabilities**:
  - Translate MCP commands to AWS API calls
  - Handle authentication and authorization
  - Return structured data to AI assistant

### 4. AWS Services
- **ECS/ECR**: Container orchestration and registry
- **Secrets Manager**: Secure configuration storage
- **CloudWatch**: Logging and monitoring
- **RDS/ElastiCache**: Database and caching
- **ALB**: Load balancing
- **IAM**: Access control

## Data Flow

### Query Flow
```
1. User → Cursor IDE
   "Check the status of the gateway ECS service"

2. Cursor IDE → AI Assistant
   Process natural language query

3. AI Assistant → AWS MCP Server (via MCP Protocol)
   {
     "service": "ecs",
     "action": "describe-services",
     "params": {
       "cluster": "codeguardians-gateway-cluster",
       "services": ["codeguardians-gateway-service"]
     }
   }

4. AWS MCP Server → AWS API
   aws ecs describe-services \
     --cluster codeguardians-gateway-cluster \
     --services codeguardians-gateway-service

5. AWS API → AWS MCP Server
   {
     "services": [{
       "serviceName": "codeguardians-gateway-service",
       "status": "ACTIVE",
       "runningCount": 2,
       "desiredCount": 2,
       "healthStatus": "HEALTHY"
     }]
   }

6. AWS MCP Server → AI Assistant
   Structured service data

7. AI Assistant → Cursor IDE → User
   "The gateway service is running healthy with 2/2 tasks active."
```

## Security Architecture

### Authentication Chain
```
User Credentials
    ↓
AWS CLI Configuration (~/.aws/credentials)
    ↓
Environment Variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    ↓
AWS MCP Server (Authenticated Session)
    ↓
AWS API (IAM Policy Enforcement)
    ↓
AWS Resources (Accessed)
```

### Security Layers

1. **User Authentication**
   - AWS IAM user credentials
   - MFA enabled (recommended)
   - Regular credential rotation

2. **IAM Permissions**
   - Least privilege principle
   - Read-only access preferred
   - Service-specific permissions

3. **MCP Server**
   - No credential storage
   - Uses AWS CLI configuration
   - Session-based authentication

4. **Network Security**
   - HTTPS for all API calls
   - AWS VPC for resources
   - Security groups and NACLs

## Configuration Structure

### `.cursor/mcp-config.json`
```json
{
  "mcpServers": {
    "aws": {
      "command": "npx",                    // Runtime
      "args": ["-y", "..."],               // Package
      "env": {                              // Environment
        "AWS_REGION": "us-east-1",
        "AWS_PROFILE": "default"
      },
      "capabilities": { ... }               // Permissions
    }
  },
  "project": {                              // Project Context
    "aws": {
      "services": { ... }                   // Resource Mapping
    }
  }
}
```

## Resource Mapping

### AIGuards Infrastructure → MCP Configuration

| AIGuards Resource | AWS Service | MCP Access |
|------------------|-------------|------------|
| Gateway Service | ECS Service: `codeguardians-gateway-service` |  Read/Monitor |
| Guard Services | ECS Tasks in cluster |  Read/Monitor |
| Container Images | ECR Repositories (6 repos) |  Read/List |
| Secrets | Secrets Manager: `codeguardians-gateway/production` |  Read |
| Database | RDS PostgreSQL (via secrets) |  Describe |
| Cache | ElastiCache Redis (via secrets) |  Describe |
| Logs | CloudWatch: `/ecs/codeguardians-gateway` |  Read/Query |
| Load Balancer | ALB (if configured) |  Describe |

## Capability Matrix

| Service | List | Describe | Create | Update | Delete |
|---------|------|----------|--------|--------|--------|
| ECS Clusters |  |  |  |  |  |
| ECS Services |  |  |  |  |  |
| ECS Tasks |  |  |  |  |  |
| ECR Repos |  |  |  |  |  |
| ECR Images |  |  |  |  |  |
| Secrets |  |  |  |  |  |
| Logs |  |  |  |  |  |
| RDS |  |  |  |  |  |
| ElastiCache |  |  |  |  |  |

*Note: MCP server is configured for read-only access for safety*

## Performance Considerations

### Caching
- MCP server may cache AWS API responses
- Cache TTL: Typically 30-60 seconds
- Explicit refresh available via queries

### Rate Limiting
- AWS API rate limits apply
- Throttling handled by AWS SDK
- Exponential backoff on errors

### Response Time
- Typical query: 500ms - 2s
- Complex queries: 2s - 5s
- Factors: Network latency, API response time, data processing

## Troubleshooting Architecture

### Common Issues and Solutions

```
Issue: MCP Server Not Starting
 Check: Node.js installed
 Check: NPX accessible
 Check: mcp-config.json valid
 Check: Cursor console logs

Issue: Permission Denied
 Check: AWS credentials configured
 Check: IAM permissions match policy
 Check: AWS region correct
 Check: Resource exists in account

Issue: Timeout Errors
 Check: Network connectivity
 Check: AWS service availability
 Check: API rate limits
 Check: Request complexity
```

## Integration with AIGuards

### Development Workflow
```
1. Developer → AI: "Deploy latest changes to ECS"
   ↓
2. AI → MCP: List current ECS services
   ↓
3. AI → Developer: Current status report
   ↓
4. Developer → AI: "Push new images to ECR"
   ↓
5. AI → MCP: List ECR repositories
   ↓
6. AI → Developer: Guide deployment process
```

### Monitoring Workflow
```
1. AI → MCP: Check ECS service health
   ↓
2. MCP → AWS: Get service status
   ↓
3. AI → MCP: Get CloudWatch logs
   ↓
4. MCP → AWS: Retrieve recent logs
   ↓
5. AI → Developer: Health report + recommendations
```

## Future Enhancements

### Planned
- [ ] Write operations (with approval)
- [ ] Deployment automation
- [ ] Cost analysis queries
- [ ] Security scanning integration
- [ ] Custom resource tagging

### Under Consideration
- [ ] Multi-region support
- [ ] CloudFormation integration
- [ ] S3 bucket management
- [ ] Lambda function queries
- [ ] Cost optimization recommendations

## Documentation References

- **Setup Guide**: `.cursor/aws-mcp-setup.md`
- **Quick Start**: `.cursor/QUICK_START.md`
- **DevOps Guide**: `../DEVOPS_GUIDE.md`
- **AWS Architecture**: `../codeguardians-gateway/codeguardians-gateway/docs/AWS_DEPLOYMENT_ARCHITECTURE.md`

---

*This architecture enables seamless AI-powered interaction with AWS infrastructure while maintaining security and best practices.*


