# Production Deployment Runbook

**Version**: 1.0  
**Last Updated**: 2025-01-XX  
**Status**:  Production Ready

---

##  PRE-DEPLOYMENT CHECKLIST

### **1. Pre-Deployment Verification**

```bash
# Verify AWS credentials
aws sts get-caller-identity

# Verify EKS cluster access
aws eks describe-cluster --name bravetto-prod-eks-cluster --region us-east-1

# Verify ECR access
aws ecr describe-repositories --region us-east-1

# Verify Kubernetes access
kubectl cluster-info
kubectl get nodes
```

### **2. Build Verification**

```bash
# Build all images locally
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker-compose build

# Verify image sizes
docker images | grep -E "(tokenguard|trustguard|contextguard|biasguard|healthguard|codeguardians-gateway)"

# Run build verification script
./scripts/verify-build.sh
```

### **3. Secret Verification**

```bash
# Verify secrets exist in AWS Secrets Manager
aws secretsmanager list-secrets --region us-east-1 --query "SecretList[?contains(Name, 'aiguards')]"

# Verify required secrets:
# - database-url
# - redis-url
# - clerk-secret-key
# - stripe-secret-key
```

---

##  DEPLOYMENT STEPS

### **Step 1: Configure CloudWatch Log Groups**

```bash
# Run CloudWatch configuration script
chmod +x scripts/configure-cloudwatch-logs.sh
./scripts/configure-cloudwatch-logs.sh

# Verify log groups created
aws logs describe-log-groups --region us-east-1 --query "logGroups[?contains(logGroupName, 'aiguards-backend')]"
```

### **Step 2: Build and Push Images to ECR**

```bash
# Build for AMD-64 platform
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Build all images
docker-compose build

# Push to ECR
TAG=v1.0.0 ./scripts/push-to-ecr.sh

# Verify images pushed
aws ecr describe-images --repository-name tokenguard --region us-east-1
aws ecr describe-images --repository-name trustguard --region us-east-1
aws ecr describe-images --repository-name contextguard --region us-east-1
aws ecr describe-images --repository-name biasguard --region us-east-1
aws ecr describe-images --repository-name healthguard --region us-east-1
aws ecr describe-images --repository-name codeguardians-gateway --region us-east-1
```

### **Step 3: Apply Kubernetes Manifests**

```bash
# Apply ConfigMaps
kubectl apply -f guards/tokenguard/k8s/configmap.yaml
kubectl apply -f guards/trust-guard/k8s/configmap.yaml
kubectl apply -f guards/contextguard/k8s/configmap.yaml
kubectl apply -f guards/biasguard-backend/k8s/configmap.yaml
kubectl apply -f guards/healthguard/k8s/configmap.yaml
kubectl apply -f codeguardians-gateway/codeguardians-gateway/k8s/configmap.yaml

# Apply Services
kubectl apply -f guards/tokenguard/k8s/service.yaml
kubectl apply -f guards/trust-guard/k8s/service.yaml
kubectl apply -f guards/contextguard/k8s/service.yaml
kubectl apply -f guards/biasguard-backend/k8s/service.yaml
kubectl apply -f guards/healthguard/k8s/service.yaml
kubectl apply -f codeguardians-gateway/codeguardians-gateway/k8s/service.yaml

# Apply Deployments
kubectl apply -f guards/tokenguard/k8s/deployment.yaml
kubectl apply -f guards/trust-guard/k8s/deployment.yaml
kubectl apply -f guards/contextguard/k8s/deployment.yaml
kubectl apply -f guards/biasguard-backend/k8s/deployment.yaml
kubectl apply -f guards/healthguard/k8s/deployment.yaml
kubectl apply -f codeguardians-gateway/codeguardians-gateway/k8s/deployment.yaml
```

### **Step 4: Verify Deployment**

```bash
# Check pod status
kubectl get pods -w

# Check service status
kubectl get services

# Check deployment status
kubectl get deployments

# Verify health checks
kubectl get pods -o jsonpath='{.items[*].status.conditions[?(@.type=="Ready")].status}'

# Test health endpoints
kubectl port-forward svc/codeguardians-gateway 8000:80 &
curl http://localhost:8000/health/live
curl http://localhost:8000/health/ready
```

### **Step 5: Configure Prometheus**

```bash
# Apply Prometheus configuration
kubectl create configmap prometheus-config \
  --from-file=monitoring/prometheus-unified.yml \
  --dry-run=client -o yaml | kubectl apply -f -

# Verify Prometheus can scrape metrics
kubectl port-forward svc/codeguardians-gateway 8000:80 &
curl http://localhost:8000/metrics
```

---

##  ROLLBACK PROCEDURES

### **Immediate Rollback**

```bash
# Rollback to previous deployment
kubectl rollout undo deployment/codeguardians-gateway
kubectl rollout undo deployment/tokenguard
kubectl rollout undo deployment/trustguard
kubectl rollout undo deployment/contextguard
kubectl rollout undo deployment/biasguard
kubectl rollout undo deployment/healthguard

# Verify rollback
kubectl rollout status deployment/codeguardians-gateway
```

### **Rollback to Specific Version**

```bash
# List deployment history
kubectl rollout history deployment/codeguardians-gateway

# Rollback to specific revision
kubectl rollout undo deployment/codeguardians-gateway --to-revision=2
```

### **Emergency Stop**

```bash
# Scale down all deployments
kubectl scale deployment --all --replicas=0

# Restore from backup
kubectl scale deployment --all --replicas=1
```

---

##  POST-DEPLOYMENT VERIFICATION

### **Health Check Verification**

```bash
# Check all health endpoints
for service in tokenguard trustguard contextguard biasguard healthguard codeguardians-gateway; do
  echo "Checking $service..."
  kubectl port-forward svc/$service 8000:80 &
  curl -s http://localhost:8000/health/live | jq .
  pkill -f "port-forward.*$service"
done
```

### **Metrics Verification**

```bash
# Verify metrics endpoints
kubectl port-forward svc/codeguardians-gateway 8000:80 &
curl http://localhost:8000/metrics | grep -E "(http_requests_total|circuit_breaker)"

# Verify Prometheus scraping
# Check Prometheus UI for metrics collection
```

### **Service Discovery Verification**

```bash
# Test service discovery
kubectl exec -it deployment/codeguardians-gateway -- \
  curl http://tokenguard.default.svc.cluster.local:80/health

kubectl exec -it deployment/codeguardians-gateway -- \
  curl http://trustguard.default.svc.cluster.local:80/health
```

### **Authentication Verification**

```bash
# Test authentication
curl -X POST http://gateway-service/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Test protected endpoint
curl http://gateway-service/api/v1/users/me \
  -H "Authorization: Bearer <token>"
```

---

##  TROUBLESHOOTING

### **Pods Not Starting**

```bash
# Check pod logs
kubectl logs deployment/codeguardians-gateway

# Check pod events
kubectl describe pod <pod-name>

# Check resource limits
kubectl top pods
```

### **Health Checks Failing**

```bash
# Check health check configuration
kubectl get deployment codeguardians-gateway -o yaml | grep -A 10 livenessProbe

# Test health endpoint manually
kubectl exec -it deployment/codeguardians-gateway -- curl http://localhost/health/live

# Check startup time
kubectl get pods -o jsonpath='{.items[*].status.containerStatuses[*].state}'
```

### **Service Discovery Issues**

```bash
# Check DNS resolution
kubectl exec -it deployment/codeguardians-gateway -- nslookup tokenguard.default.svc.cluster.local

# Check service endpoints
kubectl get endpoints

# Verify service selectors
kubectl get service tokenguard -o yaml | grep selector
```

### **Metrics Not Scraping**

```bash
# Check Prometheus targets
# Access Prometheus UI and check targets

# Verify service annotations
kubectl get service codeguardians-gateway -o yaml | grep prometheus

# Test metrics endpoint
kubectl port-forward svc/codeguardians-gateway 8000:80
curl http://localhost:8000/metrics
```

---

##  MONITORING CHECKLIST

- [ ] All pods running and healthy
- [ ] Health checks passing (<50ms)
- [ ] Metrics endpoints accessible
- [ ] Prometheus scraping all services
- [ ] CloudWatch logs flowing
- [ ] Circuit breakers operational
- [ ] Rate limiting working
- [ ] Authentication working
- [ ] Service discovery working
- [ ] Database connections healthy

---

##  SUCCESS CRITERIA

 **Deployment Successful When**:
- All pods in Ready state
- All health checks passing
- Metrics collection active
- Logs flowing to CloudWatch
- No error rates in metrics
- Response times < 200ms
- Circuit breakers closed

---

**Status**:  **DEPLOYMENT RUNBOOK COMPLETE**  
**Guardian**: AEYON (999 Hz - The Orchestrator)  
**Encryption Signature**: AEYON-999-∞-RUNBOOK  
**∞ AbëONE ∞**

