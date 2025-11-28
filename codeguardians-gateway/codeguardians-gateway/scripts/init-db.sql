-- Initialize CodeGuardians Gateway Database
-- This script sets up the database schema and initial data

-- Create the database if it doesn't exist (PostgreSQL will create it automatically)
-- The database name is set via POSTGRES_DB environment variable

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create the main application schema
CREATE SCHEMA IF NOT EXISTS codeguardians_gateway;

-- Set search path
SET search_path TO codeguardians_gateway, public;

-- Create initial tables (these will be managed by Alembic migrations)
-- This is just a placeholder for any initial setup needed

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE "codeguardians-gateway_db" TO codeguardians_gateway;
GRANT ALL PRIVILEGES ON SCHEMA codeguardians_gateway TO codeguardians_gateway;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA codeguardians_gateway TO codeguardians_gateway;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA codeguardians_gateway TO codeguardians_gateway;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA codeguardians_gateway GRANT ALL ON TABLES TO codeguardians_gateway;
ALTER DEFAULT PRIVILEGES IN SCHEMA codeguardians_gateway GRANT ALL ON SEQUENCES TO codeguardians_gateway;
