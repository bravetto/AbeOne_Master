#!/bin/bash
# CloudWatch Log Groups Configuration Script
# Creates log groups for all services with retention policies

set -e

REGION="${AWS_REGION:-us-east-1}"
RETENTION_DAYS="${LOG_RETENTION_DAYS:-7}"

SERVICES=(
    "codeguardians-gateway"
    "tokenguard"
    "trustguard"
    "contextguard"
    "biasguard"
    "healthguard"
)

echo " Configuring CloudWatch Log Groups..."
echo "Region: $REGION"
echo "Retention: $RETENTION_DAYS days"
echo ""

for service in "${SERVICES[@]}"; do
    LOG_GROUP_NAME="/aws/eks/aiguards-backend/$service"
    
    echo " Creating log group: $LOG_GROUP_NAME"
    
    # Create log group if it doesn't exist
    if ! aws logs describe-log-groups \
        --log-group-name-prefix "$LOG_GROUP_NAME" \
        --region "$REGION" \
        --query "logGroups[?logGroupName=='$LOG_GROUP_NAME']" \
        --output text | grep -q "$LOG_GROUP_NAME"; then
        
        aws logs create-log-group \
            --log-group-name "$LOG_GROUP_NAME" \
            --region "$REGION" || echo "  Log group may already exist"
    fi
    
    # Set retention policy
    echo "   Setting retention: $RETENTION_DAYS days"
    aws logs put-retention-policy \
        --log-group-name "$LOG_GROUP_NAME" \
        --retention-in-days "$RETENTION_DAYS" \
        --region "$REGION" || echo "  Failed to set retention"
    
    echo "    Configured: $LOG_GROUP_NAME"
    echo ""
done

echo " CloudWatch log groups configured successfully!"

