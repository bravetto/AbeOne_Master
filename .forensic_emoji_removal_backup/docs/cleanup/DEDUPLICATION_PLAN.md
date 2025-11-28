# Codebase Deduplication Plan

## 🎯 **Duplication Analysis**

### **1. Configuration Files (High Priority)**
- **Multiple config classes**: `config.py`, `centralized_config.py`, `dynamic_config.py`
- **Duplicate environment files**: `env.unified`, `env.example`, `test.env`
- **Multiple Docker Compose files**: 4 different compose files with overlapping services

### **2. Docker Compose Files (High Priority)**
- `docker-compose.yml` - Main single container
- `docker-compose.centralized.yml` - Multi-container with local services
- `docker-compose.integrated.yml` - Integrated services
- `docker-compose.simple-centralized.yml` - Simplified centralized

### **3. Service Configurations (Medium Priority)**
- Each guard service has its own config file
- Duplicate database connection logic
- Repeated environment variable patterns

## 📋 **Consolidation Strategy**

### **Phase 1: Configuration Consolidation**
1. **Merge config classes** into single `UnifiedConfig`
2. **Consolidate environment files** into single `.env.template`
3. **Create configuration inheritance** for different environments

### **Phase 2: Docker Compose Consolidation**
1. **Single docker-compose.yml** with profiles for different deployments
2. **Remove redundant compose files**
3. **Use environment-specific overrides**

### **Phase 3: Service Configuration Unification**
1. **Shared configuration base class**
2. **Common environment variable patterns**
3. **Unified database connection logic**

## 🚀 **Implementation Plan**

### **Step 1: Create Unified Configuration**
- Single `UnifiedConfig` class with all settings
- Environment-specific inheritance
- AWS Secrets Manager integration

### **Step 2: Consolidate Docker Compose**
- Single `docker-compose.yml` with profiles
- Environment-specific overrides
- Remove duplicate files

### **Step 3: Unify Environment Files**
- Single `.env.template` file
- Environment-specific overrides
- Clear documentation

### **Step 4: Service Configuration Sharing**
- Shared configuration utilities
- Common database connection patterns
- Unified logging and monitoring
