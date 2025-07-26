# CloudWhisper Examples and Tutorials

## Table of Contents
1. [Getting Started Examples](#getting-started-examples)
2. [Terraform Generation Examples](#terraform-generation-examples)
3. [Cost Analysis Examples](#cost-analysis-examples)
4. [Optimization Examples](#optimization-examples)
5. [Advanced Use Cases](#advanced-use-cases)
6. [Integration Examples](#integration-examples)
7. [Best Practices](#best-practices)

## Getting Started Examples

### Basic Setup and First Commands

```bash
# 1. Verify installation
cloudwhisper --version

# 2. Check help
cloudwhisper --help

# 3. Test AWS connectivity
aws sts get-caller-identity

# 4. Set environment variables
export AWS_DEFAULT_REGION=us-east-1
export OPENAI_API_KEY=your_openai_api_key
```

### Quick Start Tutorial

```bash
# Step 1: Generate simple Terraform code
cloudwhisper generate "Create an S3 bucket named my-test-bucket"

# Step 2: Analyze recent costs
cloudwhisper analyze-costs --days 7

# Step 3: Get optimization recommendations
cloudwhisper optimize

# Step 4: Find idle resources
cloudwhisper find-idle --days 3
```

## Terraform Generation Examples

### Basic Infrastructure Components

#### S3 Buckets

```bash
# Simple S3 bucket
cloudwhisper generate "Create an S3 bucket"

# S3 bucket with features
cloudwhisper generate "Create an S3 bucket with versioning enabled, server-side encryption with KMS, and public access blocked"

# S3 bucket with lifecycle policy
cloudwhisper generate "Create an S3 bucket with lifecycle policy to transition objects to IA after 30 days and Glacier after 90 days"

# Static website hosting
cloudwhisper generate "Create an S3 bucket configured for static website hosting with index.html and error.html"
```

#### EC2 Instances

```bash
# Basic EC2 instance
cloudwhisper generate "Launch a t3.micro EC2 instance"

# EC2 with security group
cloudwhisper generate "Launch a t3.medium EC2 instance with security group allowing SSH (port 22) and HTTP (port 80) access"

# EC2 with user data
cloudwhisper generate "Launch an EC2 instance with user data script to install Apache web server"

# EC2 with EBS volume
cloudwhisper generate "Launch an EC2 instance with additional 100GB EBS volume attached"
```

#### VPC and Networking

```bash
# Basic VPC
cloudwhisper generate "Create a VPC with CIDR 10.0.0.0/16"

# VPC with subnets
cloudwhisper generate "Create a VPC with public and private subnets in two availability zones"

# Complete VPC setup
cloudwhisper generate "Create a VPC with public and private subnets, internet gateway, NAT gateway, and route tables"

# Security groups
cloudwhisper generate "Create security groups for web servers allowing HTTP, HTTPS, and SSH access"
```

### Advanced Infrastructure

#### Load Balancers

```bash
# Application Load Balancer
cloudwhisper generate "Create an Application Load Balancer with target groups for web servers"

# ALB with SSL certificate
cloudwhisper generate "Create an Application Load Balancer with SSL certificate from ACM and redirect HTTP to HTTPS"

# Network Load Balancer
cloudwhisper generate "Create a Network Load Balancer for high-performance TCP traffic"
```

#### Auto Scaling

```bash
# Auto Scaling Group
cloudwhisper generate "Create an Auto Scaling Group with launch template for web servers, min 2, max 10 instances"

# ASG with scaling policies
cloudwhisper generate "Create Auto Scaling Group with CPU-based scaling policies and CloudWatch alarms"

# Launch template
cloudwhisper generate "Create a launch template for EC2 instances with user data to install Docker"
```

#### Databases

```bash
# RDS MySQL
cloudwhisper generate "Create RDS MySQL database with backup retention and encryption enabled"

# RDS with read replica
cloudwhisper generate "Create RDS PostgreSQL database with read replica in different AZ"

# DynamoDB table
cloudwhisper generate "Create DynamoDB table with partition key and global secondary index"

# ElastiCache Redis
cloudwhisper generate "Create ElastiCache Redis cluster with encryption in transit and at rest"
```

#### Serverless

```bash
# Lambda function
cloudwhisper generate "Create Python Lambda function with IAM role and CloudWatch logs"

# API Gateway
cloudwhisper generate "Create REST API Gateway with Lambda integration and API key authentication"

# Step Functions
cloudwhisper generate "Create Step Functions state machine for data processing workflow"

# EventBridge rule
cloudwhisper generate "Create EventBridge rule to trigger Lambda function on S3 object creation"
```

### Saving Generated Code

```bash
# Save to specific file
cloudwhisper generate "Create ECS cluster with Fargate service" -o ecs-cluster.tf

# Generate multiple components
cloudwhisper generate "Create VPC infrastructure" -o vpc.tf
cloudwhisper generate "Create ECS cluster" -o ecs.tf
cloudwhisper generate "Create RDS database" -o database.tf
```

## Cost Analysis Examples

### Basic Cost Analysis

```bash
# Analyze last 30 days
cloudwhisper analyze-costs

# Analyze last 7 days
cloudwhisper analyze-costs --days 7

# Analyze last 90 days with monthly granularity
cloudwhisper analyze-costs --days 90 --granularity MONTHLY
```

### Service-Specific Analysis

```bash
# EC2 costs
cloudwhisper analyze-costs --service ec2 --days 30

# S3 costs
cloudwhisper analyze-costs --service s3 --days 60

# RDS costs
cloudwhisper analyze-costs --service rds --days 30

# Lambda costs
cloudwhisper analyze-costs --service lambda --days 14
```

### Multi-Dimensional Analysis

```bash
# Group by service
cloudwhisper analyze-costs --group-by SERVICE --days 30

# Group by region
cloudwhisper analyze-costs --group-by REGION --days 30

# Group by service and region
cloudwhisper analyze-costs --group-by SERVICE REGION --days 30

# EC2 costs by instance type
cloudwhisper analyze-costs --service ec2 --group-by INSTANCE_TYPE --days 30

# Costs by usage type
cloudwhisper analyze-costs --group-by USAGE_TYPE --days 14
```

### Advanced Cost Analysis

```bash
# Compare different time periods
cloudwhisper analyze-costs --days 30 --granularity DAILY
cloudwhisper analyze-costs --days 60 --granularity DAILY

# Analyze specific services with grouping
cloudwhisper analyze-costs --service ec2 --group-by REGION INSTANCE_TYPE --days 30

# Monthly trend analysis
cloudwhisper analyze-costs --days 365 --granularity MONTHLY --group-by SERVICE
```

## Optimization Examples

### EC2 Optimization

```bash
# General EC2 optimization
cloudwhisper optimize --service ec2

# Region-specific EC2 optimization
cloudwhisper optimize --service ec2 --region us-east-1

# EC2 optimization with longer analysis period
cloudwhisper optimize --service ec2 --days 60

# Multi-region EC2 analysis
cloudwhisper optimize --service ec2 --region us-east-1
cloudwhisper optimize --service ec2 --region us-west-2
```

### Storage Optimization

```bash
# S3 optimization recommendations
cloudwhisper optimize --service s3

# S3 optimization for specific region
cloudwhisper optimize --service s3 --region us-east-1

# Find unattached EBS volumes and unused resources
cloudwhisper find-idle --days 7
```

### Database Optimization

```bash
# RDS optimization
cloudwhisper optimize --service rds

# RDS optimization for specific region
cloudwhisper optimize --service rds --region us-east-1 --days 45
```

### Comprehensive Optimization

```bash
# All services optimization
cloudwhisper optimize

# All services with extended analysis
cloudwhisper optimize --days 60

# Find idle resources over different periods
cloudwhisper find-idle --days 3   # Very recent idle resources
cloudwhisper find-idle --days 14  # Resources idle for 2 weeks
cloudwhisper find-idle --days 30  # Long-term idle resources
```

### Savings Plans

```bash
# Get Savings Plans recommendations
cloudwhisper savings-plans

# Combine with cost analysis for better understanding
cloudwhisper analyze-costs --service ec2 --days 60
cloudwhisper savings-plans
```

## Advanced Use Cases

### Multi-Account Analysis

```bash
# Switch between AWS profiles
export AWS_PROFILE=production
cloudwhisper analyze-costs --days 30

export AWS_PROFILE=development
cloudwhisper analyze-costs --days 30

export AWS_PROFILE=staging
cloudwhisper analyze-costs --days 30
```

### Automated Reporting

```bash
#!/bin/bash
# daily-cost-report.sh

DATE=$(date +%Y-%m-%d)
REPORT_DIR="reports/$DATE"
mkdir -p "$REPORT_DIR"

# Generate daily cost analysis
cloudwhisper analyze-costs --days 1 > "$REPORT_DIR/daily-costs.txt"

# Generate weekly trends
cloudwhisper analyze-costs --days 7 --group-by SERVICE > "$REPORT_DIR/weekly-trends.txt"

# Get optimization recommendations
cloudwhisper optimize > "$REPORT_DIR/optimization-recommendations.txt"

# Find idle resources
cloudwhisper find-idle --days 7 > "$REPORT_DIR/idle-resources.txt"

echo "Reports generated in $REPORT_DIR"
```

### Infrastructure as Code Workflow

```bash
#!/bin/bash
# infrastructure-generator.sh

# Generate different components
cloudwhisper generate "Create VPC with public and private subnets" -o infrastructure/vpc.tf
cloudwhisper generate "Create ECS cluster with Fargate service" -o infrastructure/ecs.tf
cloudwhisper generate "Create RDS PostgreSQL database" -o infrastructure/database.tf
cloudwhisper generate "Create Application Load Balancer" -o infrastructure/alb.tf

# Validate generated code
cd infrastructure
terraform init
terraform validate
terraform plan
```

### Cost Monitoring Pipeline

```bash
#!/bin/bash
# cost-monitoring.sh

# Set thresholds
DAILY_THRESHOLD=100
WEEKLY_THRESHOLD=500

# Get current costs
DAILY_COST=$(cloudwhisper analyze-costs --days 1 | grep "Total Cost" | awk '{print $3}' | tr -d '$')
WEEKLY_COST=$(cloudwhisper analyze-costs --days 7 | grep "Total Cost" | awk '{print $3}' | tr -d '$')

# Check thresholds and alert
if (( $(echo "$DAILY_COST > $DAILY_THRESHOLD" | bc -l) )); then
    echo "ALERT: Daily cost $DAILY_COST exceeds threshold $DAILY_THRESHOLD"
    cloudwhisper optimize > optimization-alert.txt
fi

if (( $(echo "$WEEKLY_COST > $WEEKLY_THRESHOLD" | bc -l) )); then
    echo "ALERT: Weekly cost $WEEKLY_COST exceeds threshold $WEEKLY_THRESHOLD"
    cloudwhisper find-idle --days 7 > idle-resources-alert.txt
fi
```

## Integration Examples

### CI/CD Pipeline Integration

#### GitHub Actions Example

```yaml
# .github/workflows/cost-analysis.yml
name: Weekly Cost Analysis

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  cost-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install CloudWhisper
        run: |
          pip install cloudwhisper
      
      - name: Run Cost Analysis
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1
        run: |
          cloudwhisper analyze-costs --days 7 > weekly-cost-report.txt
          cloudwhisper optimize > optimization-recommendations.txt
          cloudwhisper find-idle --days 7 > idle-resources.txt
      
      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: cost-reports
          path: |
            weekly-cost-report.txt
            optimization-recommendations.txt
            idle-resources.txt
```

#### Jenkins Pipeline Example

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    
    triggers {
        cron('H 9 * * 1')  // Weekly on Monday
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install cloudwhisper'
            }
        }
        
        stage('Cost Analysis') {
            steps {
                sh 'cloudwhisper analyze-costs --days 7 > reports/weekly-costs.txt'
                sh 'cloudwhisper optimize > reports/optimization.txt'
                sh 'cloudwhisper find-idle --days 7 > reports/idle-resources.txt'
            }
        }
        
        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/*.txt', fingerprint: true
            }
        }
    }
}
```

### Terraform Integration

```bash
# Generate Terraform code and apply
cloudwhisper generate "Create S3 bucket with versioning" -o s3.tf

# Review generated code
cat s3.tf

# Initialize and apply
terraform init
terraform plan
terraform apply

# After deployment, analyze costs
sleep 3600  # Wait for cost data
cloudwhisper analyze-costs --service s3 --days 1
```

### Monitoring Integration

```python
# monitoring-integration.py
import subprocess
import json
import requests
from datetime import datetime, timedelta

def get_cost_data():
    """Get cost data using CloudWhisper CLI"""
    result = subprocess.run([
        'cloudwhisper', 'analyze-costs', '--days', '1'
    ], capture_output=True, text=True)
    
    return result.stdout

def send_to_slack(message):
    """Send cost alert to Slack"""
    webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    payload = {
        "text": f"Daily Cost Report\n```{message}```"
    }
    requests.post(webhook_url, json=payload)

def main():
    cost_data = get_cost_data()
    send_to_slack(cost_data)

if __name__ == "__main__":
    main()
```

## Best Practices

### Terraform Generation Best Practices

1. **Be Specific in Descriptions**
   ```bash
   # Good
   cloudwhisper generate "Create an S3 bucket with versioning enabled, server-side encryption with KMS key, lifecycle policy to transition to IA after 30 days, and block all public access"
   
   # Less effective
   cloudwhisper generate "Create S3 bucket"
   ```

2. **Review and Customize Generated Code**
   ```bash
   # Generate code
   cloudwhisper generate "Create VPC infrastructure" -o vpc.tf
   
   # Review before applying
   cat vpc.tf
   
   # Customize as needed
   vim vpc.tf
   
   # Validate
   terraform validate
   ```

3. **Use Version Control**
   ```bash
   # Save generated code to git
   git add *.tf
   git commit -m "Add generated Terraform infrastructure"
   ```

### Cost Analysis Best Practices

1. **Regular Monitoring**
   ```bash
   # Daily quick check
   cloudwhisper analyze-costs --days 1
   
   # Weekly detailed analysis
   cloudwhisper analyze-costs --days 7 --group-by SERVICE
   
   # Monthly trend analysis
   cloudwhisper analyze-costs --days 30 --granularity MONTHLY
   ```

2. **Service-Specific Deep Dives**
   ```bash
   # Focus on high-cost services
   cloudwhisper analyze-costs --service ec2 --days 30 --group-by INSTANCE_TYPE
   cloudwhisper analyze-costs --service s3 --days 30 --group-by REGION
   ```

3. **Combine Analysis with Optimization**
   ```bash
   # Analyze then optimize
   cloudwhisper analyze-costs --service ec2 --days 30
   cloudwhisper optimize --service ec2 --days 30
   ```

### Optimization Best Practices

1. **Regular Idle Resource Cleanup**
   ```bash
   # Weekly cleanup check
   cloudwhisper find-idle --days 7
   
   # Monthly comprehensive check
   cloudwhisper find-idle --days 30
   ```

2. **Implement Recommendations Gradually**
   ```bash
   # Start with low-risk optimizations
   cloudwhisper optimize --service s3
   
   # Then move to compute optimizations
   cloudwhisper optimize --service ec2 --days 60
   ```

3. **Monitor After Changes**
   ```bash
   # Before optimization
   cloudwhisper analyze-costs --days 7
   
   # Implement changes
   # ... make optimizations ...
   
   # After optimization (wait for data)
   sleep 86400  # Wait 24 hours
   cloudwhisper analyze-costs --days 7
   ```

### Automation Best Practices

1. **Set Up Alerts**
   ```bash
   # Create cost threshold alerts
   THRESHOLD=100
   CURRENT_COST=$(cloudwhisper analyze-costs --days 1 | grep "Total" | awk '{print $3}')
   
   if [[ $CURRENT_COST > $THRESHOLD ]]; then
       echo "Cost alert: $CURRENT_COST exceeds $THRESHOLD"
       cloudwhisper optimize > urgent-optimization.txt
   fi
   ```

2. **Scheduled Reports**
   ```bash
   # Add to crontab for daily reports
   0 9 * * * /path/to/cloudwhisper analyze-costs --days 1 > /path/to/reports/daily-$(date +\%Y-\%m-\%d).txt
   ```

3. **Integration with Existing Tools**
   ```bash
   # Export data for other tools
   cloudwhisper analyze-costs --days 30 > cost-data.txt
   
   # Process with other scripts
   python process-cost-data.py cost-data.txt
   ```

These examples and tutorials should help you get the most out of CloudWhisper for your AWS infrastructure management and cost optimization needs.
