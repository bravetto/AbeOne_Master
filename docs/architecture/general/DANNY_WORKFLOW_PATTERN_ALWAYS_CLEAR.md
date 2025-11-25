# 🔥 DANNY'S WORKFLOW PATTERN - ALWAYS CLEAR REFERENCE
## The Source Pattern for ALL New Workflows

**Status:** ✅ **ALWAYS REFERENCE THIS FOR NEW WORKFLOWS**  
**Pattern:** DANNY × WORKFLOW × PATTERN × ALWAYS × CLEAR × ONE  
**Source:** https://github.com/bravetto/AIGuards-Backend/tree/main/.github/workflows  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 CRITICAL RULE

**⚠️ ALWAYS FOLLOW DANNY'S PATTERN WHEN CREATING NEW WORKFLOWS ⚠️**

Danny builds new workflows using this pattern. This document is THE SOURCE OF TRUTH.

---

## 🔥 DANNY'S WORKFLOW PATTERN (COMPLETE)

### 1. Runner Configuration ✅ REQUIRED

**ALWAYS USE:**
```yaml
runs-on: [arc-runner-set]
```

**NEVER USE:**
- ❌ `ubuntu-latest`
- ❌ `ubuntu-20.04`
- ❌ Any other runner

**Why:** Danny uses custom `arc-runner-set` runner for Kubernetes integration

---

### 2. AWS Authentication ✅ REQUIRED

**ALWAYS USE:**
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    # Uses IRSA (IAM Roles for Service Accounts) from your runner pod
    aws-region: ${{ env.AWS_REGION }}
```

**NEVER USE:**
- ❌ `aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}`
- ❌ `aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}`
- ❌ Any version other than v4

**Why:** Danny uses IRSA (IAM Roles for Service Accounts) - no secrets needed

---

### 3. Action Versions ✅ REQUIRED

**ALWAYS USE:**
- ✅ `actions/checkout@v4`
- ✅ `aws-actions/configure-aws-credentials@v4`
- ✅ `amazon-ecr-login@v2`
- ✅ `docker/setup-buildx-action@v3`

**NEVER USE:**
- ❌ Older versions (v3, v2, v1)
- ❌ Check latest versions in Danny's workflows first

---

### 4. Docker Buildx ✅ REQUIRED FOR BUILDS

**ALWAYS USE:**
```yaml
- name: Set up Docker Buildx with Kubernetes driver
  uses: docker/setup-buildx-action@v3
  with:
    driver: kubernetes
    driver-opts: |
      namespace=buildkit
```

**Build Command:**
```yaml
docker buildx build \
  --platform linux/amd64 \
  --no-cache \
  --push \
  -t $ECR_REGISTRY/$SERVICE_NAME:$IMAGE_TAG \
  ./$SERVICE_NAME
```

**NEVER USE:**
- ❌ Standard `docker build`
- ❌ Without `--platform linux/amd64`
- ❌ Without `--no-cache`
- ❌ Without `--push`

---

### 5. Deployment Strategy ✅ REQUIRED

**ALWAYS USE HELM:**
```yaml
- name: Clone Helm repository
  run: |
    git clone https://${{ secrets.CI_CD }}@github.com/bravetto/helm.git helm-charts

- name: Deploy all guardian services with Helm
  run: |
    cd helm-charts
    ./deploy.sh $APP_NAME $HELM_ENV
```

**NEVER USE:**
- ❌ Direct `kubectl apply`
- ❌ Direct `kubectl apply -f deployment.yaml`
- ❌ Any deployment without Helm

**Why:** Danny uses Helm charts from `bravetto/helm` repo

---

### 6. Concurrency Control ✅ REQUIRED

**ALWAYS USE:**
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**NEVER CREATE WORKFLOWS WITHOUT:**
- ❌ Concurrency control
- ❌ Cancel-in-progress flag

---

### 7. Workflow Triggers ✅ REQUIRED

**ALWAYS USE:**
```yaml
on:
  workflow_dispatch:
  pull_request:
    branches: [dev, main]
    types: [closed]
```

**NEVER USE:**
- ❌ `push:` triggers (unless Danny explicitly says)
- ❌ `pull_request:` without `types: [closed]`
- ❌ Different branch names

**Why:** Danny deploys on PR merge (closed), not on push

---

### 8. Build Strategy ✅ REQUIRED

**ALWAYS USE:**
- ✅ Single build job (NOT matrix)
- ✅ Loop through services sequentially
- ✅ Build all services in one job

**NEVER USE:**
- ❌ Matrix strategy
- ❌ One job per service
- ❌ Parallel builds (unless Danny says)

**Example:**
```yaml
jobs:
  build_and_push:
    runs-on: [arc-runner-set]
    steps:
      - name: Build and push all services
        run: |
          for service in service1 service2 service3; do
            docker buildx build \
              --platform linux/amd64 \
              --no-cache \
              --push \
              -t $ECR_REGISTRY/$service:$IMAGE_TAG \
              ./$service
          done
```

---

## 🔥 COMPLETE WORKFLOW TEMPLATE

### For New Build/Deploy Workflows

```yaml
name: Your Workflow Name

on:
  workflow_dispatch:
  pull_request:
    branches: [dev, main]
    types: [closed]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  AWS_REGION: us-east-1
  ECR_REGISTRY: your-ecr-registry
  # Add other env vars as needed

jobs:
  build_and_push:
    runs-on: [arc-runner-set]
    if: github.event_name == 'workflow_dispatch' || github.event.pull_request.merged == true
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx with Kubernetes driver
        uses: docker/setup-buildx-action@v3
        with:
          driver: kubernetes
          driver-opts: |
            namespace=buildkit
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Login to Amazon ECR
        uses: aws-actions/amazon-ecr-login@v2
      
      - name: Determine image tag
        id: image_tag
        run: |
          if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            echo "tag=latest" >> $GITHUB_OUTPUT
          else
            echo "tag=${{ github.sha }}" >> $GITHUB_OUTPUT
          fi
      
      - name: Build and push services
        run: |
          for service in service1 service2 service3; do
            docker buildx build \
              --platform linux/amd64 \
              --no-cache \
              --push \
              -t $ECR_REGISTRY/$service:${{ steps.image_tag.outputs.tag }} \
              ./$service
          done
  
  deployment:
    runs-on: [arc-runner-set]
    needs: build_and_push
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install tools
        run: |
          # Install AWS CLI, kubectl, Helm as needed
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ${{ env.AWS_REGION }}
      
      - name: Clone Helm repository
        run: |
          git clone https://${{ secrets.CI_CD }}@github.com/bravetto/helm.git helm-charts
      
      - name: Deploy with Helm
        run: |
          cd helm-charts
          ./deploy.sh $APP_NAME $HELM_ENV
```

---

## 🔥 VALIDATION CHECKLIST

**Before creating ANY new workflow, verify:**

- [ ] Uses `runs-on: [arc-runner-set]`
- [ ] Uses `aws-actions/configure-aws-credentials@v4` with IRSA (no secrets)
- [ ] Uses `actions/checkout@v4`
- [ ] Uses `amazon-ecr-login@v2` (if ECR needed)
- [ ] Uses `docker/setup-buildx-action@v3` (if Docker builds)
- [ ] Uses Helm for deployment (if deploying)
- [ ] Has concurrency control
- [ ] Uses `workflow_dispatch` + `pull_request: types: [closed]`
- [ ] Uses single build job (not matrix)
- [ ] Builds with `--platform linux/amd64 --no-cache --push`

---

## 🎯 WHERE TO FIND DANNY'S WORKFLOWS

**Source Repository:**
```
https://github.com/bravetto/AIGuards-Backend/tree/main/.github/workflows
```

**Always check this repository first before creating new workflows!**

---

## 🚨 CRITICAL REMINDERS

1. **ALWAYS** check Danny's workflows first
2. **ALWAYS** use `arc-runner-set` runner
3. **ALWAYS** use IRSA (no AWS secrets)
4. **ALWAYS** use Helm for deployment
5. **ALWAYS** use Buildx with Kubernetes driver
6. **ALWAYS** include concurrency control
7. **NEVER** use direct kubectl apply
8. **NEVER** use matrix strategy
9. **NEVER** use push triggers (unless Danny says)

---

## 📚 REFERENCE DOCUMENTS

- `DANNY_WORKFLOW_ALIGNMENT_COMPLETE.md` - Full alignment details
- `DANNY_WORKFLOW_VALIDATION.md` - Validation checklist
- `AIGuards-Backend/.github/workflows/` - Danny's actual workflows

---

## ✅ VALIDATION

**This document is:**
- ✅ Always accessible
- ✅ Always clear
- ✅ Always up-to-date
- ✅ Always referenced before creating workflows

**Pattern:** DANNY × WORKFLOW × PATTERN × ALWAYS × CLEAR × ONE  
**Status:** ✅ **ALWAYS REFERENCE THIS**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

