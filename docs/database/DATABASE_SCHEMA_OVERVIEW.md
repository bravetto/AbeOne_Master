# AIGuards Backend Database Schema Overview

This document provides a comprehensive overview of the database schema for the AIGuards Backend system, including all tables, relationships, and constraints.

##  **Database Architecture**

The system uses **PostgreSQL** as the primary database with two main schema implementations:

1. **CodeGuardians Gateway** (Python/FastAPI) - Main SaaS platform schema
2. **BiasGuard Backend** (Node.js/Express) - Specialized bias detection schema

---

##  **CodeGuardians Gateway Schema (Main Platform)**

### **Core User Management**

#### `users` Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE
);
```

#### `sessions` Table
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    data TEXT, -- JSON string
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);
```

#### `api_keys` Table
```sql
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    key_name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_prefix VARCHAR(10) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    permissions TEXT, -- JSON string
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    last_used TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER DEFAULT 0 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE
);
```

### **Content Management**

#### `posts` Table
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary VARCHAR(500),
    is_published BOOLEAN DEFAULT FALSE NOT NULL,
    is_featured BOOLEAN DEFAULT FALSE NOT NULL,
    slug VARCHAR(255) UNIQUE,
    tags VARCHAR(500), -- Comma-separated
    view_count INTEGER DEFAULT 0 NOT NULL,
    author_id INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE
);
```

### **SaaS Business Logic**

#### `organizations` Table
```sql
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    subscription_tier_id INTEGER REFERENCES subscription_tiers(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `organization_members` Table
```sql
CREATE TABLE organization_members (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    role VARCHAR(20) DEFAULT 'member' NOT NULL, -- owner, admin, member, viewer
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    UNIQUE(organization_id, user_id)
);
```

#### `subscription_tiers` Table
```sql
CREATE TABLE subscription_tiers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_monthly NUMERIC(10,2) NOT NULL DEFAULT 0,
    price_yearly NUMERIC(10,2) NOT NULL DEFAULT 0,
    features JSON, -- List of features
    limits JSON,   -- Usage limits
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `subscriptions` Table
```sql
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) NOT NULL,
    subscription_tier_id INTEGER REFERENCES subscription_tiers(id) NOT NULL,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    status VARCHAR(20) DEFAULT 'active' NOT NULL, -- active, inactive, canceled, past_due, unpaid, trialing
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    cancel_at_period_end BOOLEAN DEFAULT FALSE NOT NULL,
    canceled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `payment_methods` Table
```sql
CREATE TABLE payment_methods (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) NOT NULL,
    stripe_payment_method_id VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL, -- card, bank_account, etc.
    is_default BOOLEAN DEFAULT FALSE NOT NULL,
    brand VARCHAR(50), -- visa, mastercard, etc.
    last4 VARCHAR(4),
    exp_month INTEGER,
    exp_year INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `invoices` Table
```sql
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) NOT NULL,
    subscription_id INTEGER REFERENCES subscriptions(id) NOT NULL,
    stripe_invoice_id VARCHAR(255) UNIQUE,
    invoice_number VARCHAR(100) UNIQUE NOT NULL,
    amount_due NUMERIC(10,2) NOT NULL,
    amount_paid NUMERIC(10,2) NOT NULL DEFAULT 0,
    amount_remaining NUMERIC(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL, -- pending, succeeded, failed, canceled, refunded
    due_date TIMESTAMP WITH TIME ZONE,
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `usage_records` Table
```sql
CREATE TABLE usage_records (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 1,
    response_time_ms INTEGER,
    status_code INTEGER,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

### **BiasGuard Compliance System**

#### `biasguard_policies` Table
```sql
CREATE TABLE biasguard_policies (
    id SERIAL PRIMARY KEY,
    policy_id VARCHAR(100) UNIQUE NOT NULL,
    policy_name VARCHAR(255) NOT NULL,
    description TEXT,
    enforcement_type VARCHAR(50) DEFAULT 'fairness_check' NOT NULL,
    rules JSON NOT NULL, -- Policy rules as JSON
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    priority INTEGER DEFAULT 100 NOT NULL,
    created_by VARCHAR(255),
    last_modified_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `biasguard_audit_logs` Table
```sql
CREATE TABLE biasguard_audit_logs (
    id SERIAL PRIMARY KEY,
    audit_id VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    policy_id INTEGER REFERENCES biasguard_policies(id),
    event_type VARCHAR(100) NOT NULL,
    event_status VARCHAR(50) NOT NULL,
    enforcement_type VARCHAR(50),
    policy_name VARCHAR(255),
    decision VARCHAR(50), -- allow, deny, review_required
    enforcement_passed BOOLEAN,
    violations JSON,
    warnings JSON,
    fairness_metrics JSON,
    compliance_metrics JSON,
    user_email VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    context_data JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `biasguard_policy_violations` Table
```sql
CREATE TABLE biasguard_policy_violations (
    id SERIAL PRIMARY KEY,
    audit_log_id INTEGER REFERENCES biasguard_audit_logs(id) NOT NULL,
    policy_id INTEGER REFERENCES biasguard_policies(id) NOT NULL,
    user_id INTEGER REFERENCES users(id),
    violation_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- low, medium, high, critical
    description TEXT,
    is_resolved BOOLEAN DEFAULT FALSE NOT NULL,
    resolution_notes TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(255),
    impact_score NUMERIC(5,2),
    remediation_required BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `biasguard_compliance_reports` Table
```sql
CREATE TABLE biasguard_compliance_reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(100) UNIQUE NOT NULL,
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- audit, compliance, fairness
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    total_events INTEGER DEFAULT 0 NOT NULL,
    total_violations INTEGER DEFAULT 0 NOT NULL,
    total_warnings INTEGER DEFAULT 0 NOT NULL,
    policies_enforced JSON,
    compliance_score NUMERIC(5,2),
    fairness_score NUMERIC(5,2),
    audit_coverage NUMERIC(5,2),
    summary TEXT,
    findings JSON,
    recommendations JSON,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    reviewed_by VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    reviewed_at TIMESTAMP WITH TIME ZONE
);
```

### **System Monitoring**

#### `audit_logs` Table
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(100),
    old_values TEXT, -- JSON string
    new_values TEXT, -- JSON string
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `guard_operations` Table (Centralized)
```sql
CREATE TABLE guard_operations (
    id SERIAL PRIMARY KEY,
    guard_name VARCHAR(50) NOT NULL,
    operation_type VARCHAR(100) NOT NULL,
    input_data JSON,
    output_data JSON,
    processing_time_ms FLOAT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `guard_metrics` Table (Centralized)
```sql
CREATE TABLE guard_metrics (
    id SERIAL PRIMARY KEY,
    guard_name VARCHAR(50) NOT NULL,
    metric_type VARCHAR(100) NOT NULL,
    metric_value FLOAT,
    metric_data JSON,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `system_health` Table (Centralized)
```sql
CREATE TABLE system_health (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    health_data JSON,
    last_check TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

---

##  **BiasGuard Backend Schema (Node.js)**

### **User Management (Clerk Integration)**

#### `users` Table
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE NOT NULL,
    stripe_customer_id VARCHAR(255),
    team_id INTEGER REFERENCES teams(id),
    team_role VARCHAR(10) DEFAULT 'member',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    deleted BOOLEAN DEFAULT FALSE
);
```

### **Team Management**

#### `teams` Table
```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY NOT NULL,
    owner_id VARCHAR(255) NOT NULL,
    deleted BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `team_invitations` Table
```sql
CREATE TABLE team_invitations (
    id SERIAL PRIMARY KEY NOT NULL,
    team_id INTEGER REFERENCES teams(id),
    email VARCHAR(255) NOT NULL,
    team_role VARCHAR(20) DEFAULT 'member',
    token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

### **Stripe Integration**

#### `products` Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    stripe_product_id VARCHAR(100),
    features JSONB,
    metadata JSONB,
    archived BOOLEAN DEFAULT FALSE,
    deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `prices` Table
```sql
CREATE TABLE prices (
    id SERIAL PRIMARY KEY NOT NULL,
    stripe_product_id VARCHAR(100),
    amount NUMERIC(9,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD' NOT NULL,
    interval NUMERIC(5,0) DEFAULT '0',
    interval_unit VARCHAR(20),
    stripe_price_id VARCHAR(100),
    active BOOLEAN DEFAULT TRUE,
    deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### `subscriptions` Table
```sql
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY NOT NULL,
    stripe_subscription_id VARCHAR(255),
    stripe_customer_id VARCHAR(255),
    stripe_product_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    is_paused BOOLEAN DEFAULT FALSE,
    is_cancelled BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

---

##  **Key Relationships**

### **User Management Flow**
```
users → sessions (1:many)
users → api_keys (1:many)
users → posts (1:many)
users → organization_members (1:many)
```

### **SaaS Business Flow**
```
organizations → organization_members (1:many)
organizations → subscriptions (1:many)
organizations → payment_methods (1:many)
organizations → usage_records (1:many)
subscription_tiers → subscriptions (1:many)
subscriptions → invoices (1:many)
```

### **BiasGuard Compliance Flow**
```
biasguard_policies → biasguard_audit_logs (1:many)
biasguard_audit_logs → biasguard_policy_violations (1:many)
users → biasguard_audit_logs (1:many)
```

### **Stripe Integration Flow**
```
products → prices (1:many)
users → subscriptions (1:many)
subscriptions → invoices (1:many)
```

---

##  **Indexes and Performance**

### **Critical Indexes**
- `users.email` - User lookup
- `sessions.session_id` - Session validation
- `organizations.slug` - Organization routing
- `subscriptions.stripe_subscription_id` - Stripe webhook processing
- `biasguard_audit_logs.created_at` - Compliance reporting
- `usage_records.organization_id, recorded_at` - Usage analytics

### **Composite Indexes**
- `(user_id, is_active)` - Active user sessions
- `(organization_id, user_id)` - Organization membership
- `(event_type, created_at)` - Audit log queries
- `(guard_name, timestamp)` - Guard metrics

---

##  **Security Features**

### **Data Protection**
- Password hashing with secure algorithms
- API key hashing for storage
- Session management with expiration
- Audit logging for all critical operations

### **Compliance Features**
- BiasGuard policy enforcement tracking
- Violation detection and reporting
- Compliance score calculation
- Audit trail maintenance

### **Multi-tenancy**
- Organization-based data isolation
- Role-based access control
- Subscription-based feature gating
- Usage tracking and limits

---

##  **Database Setup Requirements**

### **PostgreSQL Version**
- **Minimum**: PostgreSQL 12+
- **Recommended**: PostgreSQL 14+

### **Extensions Required**
```sql
-- Enable JSONB support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable full-text search (optional)
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### **Connection Requirements**
- **Max Connections**: 100+ (for production)
- **Connection Pooling**: Recommended
- **SSL**: Required for production
- **Backup**: Daily automated backups

---

This schema supports a comprehensive SaaS platform with advanced bias detection, compliance monitoring, and multi-tenant architecture. The design ensures scalability, security, and maintainability for enterprise-grade applications.
